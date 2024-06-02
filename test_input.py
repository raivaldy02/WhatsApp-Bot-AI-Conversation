import asyncio
import time

class Utility:
    save_operation = False

    @classmethod
    async def save_users(cls, data, filepath) -> bool: 
        while cls.save_operation: 
            await asyncio.sleep(0.5)
        
        cls.save_operation = True

        try: 
            print(data)
            with open(filepath, "w") as f: 
                f.write(json.dumps(data))
                f.close()
        except: 
            cls.save_operation = False
            return False
        finally: 
            await asyncio.sleep(900)
            cls.save_operation = False
        
        return True

async def save(data, filepath): 
    loop = asyncio.get_event_loop()

    for x in range(10): 
        print(x)
        result = loop.create_task(Utility.save_users(data, filepath))

    while asyncio.get_running_loop(): 
        await asyncio.sleep(3)

async def main():
    data = {"user": "John Doe"}
    filepath = "users.json"

    await save(data, filepath)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# asyncio.run(main())