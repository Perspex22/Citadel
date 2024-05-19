from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Replace these with appropriate values
api_id = 'API-ID HERE'
api_hash = 'API HASH HERE'
phone_number = 'PHONE NUMBER HERE'

# Group and channel details
source_group = 'Source channel/group username'
destination_channel = 'destination channel/group'

# Number of members to fetch at once
fetch_limit = 10

async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        # Fetch members from the source group
        participants = []
        offset = 0

        while True:
            chunk = await client(GetParticipantsRequest(
                source_group, ChannelParticipantsSearch(''), offset, fetch_limit, hash=0
            ))
            if not chunk.users:
                break
            participants.extend(chunk.users)
            offset += len(chunk.users)

        # Add fetched members to the destination channel
        for user in participants:
            try:
                await client(InviteToChannelRequest(destination_channel, [user]))
                print(f"Added {user.username or user.id} to the channel")
            except Exception as e:
                print(f"Failed to add {user.username or user.id}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
