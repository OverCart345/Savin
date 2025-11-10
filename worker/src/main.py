import asyncio
import sys

from core.database import AsyncSessionLocal
from core.redis_queue import RedisQueue
from clients.push_client import PushNotificationClient
from repositories.subscriber_repo import SubscriberRepository


async def process_notification(task: dict, db_session, push_client: PushNotificationClient):
    author_id = task.get("author_id")
    post_id = task.get("post_id")
    post_title = task.get("post_title", "")
    
    print(f"Processing notification for post {post_id} by author {author_id}")
    
    repo = SubscriberRepository(db_session)
    subscribers = await repo.get_subscribers_with_keys(author_id)
    
    if not subscribers:
        print(f"No subscribers with subscription_key for author {author_id}")
        return
    
    print(f"Found {len(subscribers)} subscribers with keys")

    short_title = post_title[:40] + "..." if len(post_title) > 40 else post_title
    message = f"Пользователь {author_id} выпустил новый пост: {short_title}"
    
    sent_count = 0
    for subscriber in subscribers:
        subscription_key = subscriber["subscription_key"]
        subscriber_id = subscriber["subscriber_id"]
        
        success = await push_client.send_notification(subscription_key, message)
        
        if success:
            sent_count += 1
            print(f"Sent notification to subscriber {subscriber_id}")
        else:
            print(f"Failed to send notification to subscriber {subscriber_id}")
    
    print(f"Notifications sent: {sent_count}/{len(subscribers)}")



async def main():
    redis_queue = RedisQueue()
    push_client = PushNotificationClient()
    
    try:
        await redis_queue.connect()

        
        while True:
            try:
                task = await redis_queue.dequeue_notification(timeout=0)
                
                if task:
                    print(f"\n📨 Received task: {task}")
                    
                    async with AsyncSessionLocal() as db_session:
                        await process_notification(task, db_session, push_client)
                    
                    print("Task completed\n")
                    
            except KeyboardInterrupt:
                print("\nShutdown requested...")
                break
            except Exception as e:
                print(f"Error processing task: {e}")
                await asyncio.sleep(1)
    
    finally:
        await redis_queue.close()
        await push_client.close()
        print("Worker stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
