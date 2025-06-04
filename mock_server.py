import asyncio, websockets, random, json

async def server(websocket):
    while True:
        data = {"ticker": "AAPL", "price": round(random.uniform(150, 200), 2)}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Update every second

async def main():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())