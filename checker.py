import requests


def read_wallets(file_path):
    wallets = []
    with open(file_path, 'r') as file:
        for line in file:
            wallets.append(line.strip())
    return wallets

wallets = read_wallets("wallets.txt")

# Base URLs for the API requests
base_activity_url = "https://www.party.app/api/user/activity"
base_crowdfund_url = "https://nft.party.app/api/crowdfund/details_for_user"



# Iterate over each address
for wallet in wallets:
    # Make the request to get user activity
    activity_url = f"{base_activity_url}?userAddress={wallet}"
    response = requests.get(activity_url)

    if response.status_code == 200:
        data = response.json()

        # Check if there are crowdfund contributions
        contributions = data.get("activity", {}).get("user", {}).get("crowdfundContributions", [])

        total_unclaimed = 0  # Running total of unclaimed amounts in ETH

        if contributions:
            # For each contribution, get the crowdfund address and amount
            for contribution in contributions:
                crowdfund_address = contribution.get("crowdfundAddress")
                eth_amount = int(contribution.get("amount", 0)) / 1e18  # Convert to ETH

                # Make the request to get crowdfund details
                crowdfund_url = f"{base_crowdfund_url}?partyCrowdfundAddress={crowdfund_address}&userAddress={wallet}"
                crowdfund_response = requests.get(crowdfund_url)

                if crowdfund_response.status_code == 200:
                    crowdfund_data = crowdfund_response.json()
                    has_claimed = crowdfund_data.get("hasClaimed", False)

                    # If not claimed, add the amount to the total
                    if not has_claimed:
                        total_unclaimed += eth_amount

                else:
                    print(f"Failed to retrieve crowdfund details for address {crowdfund_address}.")
        
        if total_unclaimed > 0:
            print(f"{wallet}, Unclaimed: {total_unclaimed}")
        else:
            print(f"{wallet}, Unclaimed: 0")
    else:
        print(f"Failed to retrieve activity for address {wallet}.")
