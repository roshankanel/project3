import streamlit as st
from web3 import Web3
import solcx

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Read solidity file
with open('./NFT_MKP.sol', 'r') as f:
    contract_source_code = f.read()

# Compile contract
compiled_contract = solcx.compile_source(contract_source_code)

# Update contract to include the contract name
contract_name = '<stdin>:NFTMarketplace'

# Access the contract interface using the correct name
contract_interface = compiled_contract[contract_name]

# Load contract ABI
contract_abi = contract_interface['abi']

# IPFS URL
ipfs_url = "https://ipfs.io/ipfs/"

# Define contract address
contract_address = None

# Define contract variable
contract = None

# Create app
st.title('NFT Marketplace')
accounts = w3.eth.accounts

# Store contract_address session state
if 'contract_address' not in st.session_state:
    st.session_state.contract_address = None

# WebUI for pages
menu = ["Deploy Marketplace Contract", "Marketplace", "Exchange"]
choice = st.sidebar.selectbox("Select an option", menu)

# Deploy Contract Page
if choice == "Deploy Marketplace Contract":
    st.write("Deploy NFT Marketplace Contract:")
    name = st.text_input("Name")
    symbol = st.text_input("Symbol")
    deployer_address = st.selectbox("Select Contract Owner Address", options=accounts)  
    if st.button("Deploy Contract"):
        contract = w3.eth.contract(abi=contract_abi, bytecode=contract_interface['bin'])
        st.session_state.deployer_address = deployer_address

        # Estimate gas for contract deployment
        estimated_gas = contract.constructor(name, symbol).estimateGas({'from': deployer_address})
        
        tx_hash = contract.constructor(name, symbol).transact({
            'from': deployer_address,
            'gas': estimated_gas,
            'gasPrice': w3.eth.gasPrice
        })

        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)  
        st.write(f"Contract deployed at address: {contract_address}")
        st.session_state.contract_address = contract_address  

# Marketplace Page
elif choice == "Marketplace":
    if st.session_state.contract_address is not None:
        contract_address = st.session_state.contract_address
        marketplace_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        marketplace_owner = st.session_state.deployer_address

        # Get marketplace details
        try:
            marketplace_name = marketplace_contract.functions.name().call()
            marketplace_symbol = marketplace_contract.functions.symbol().call()
            token_id_counter = marketplace_contract.functions.getTokenIdCounter().call()

            st.sidebar.title("NFT Marketplace Information")
            st.sidebar.write(f"Marketplace Owner: {marketplace_owner}")
            st.sidebar.write(f"Marketplace Name: {marketplace_name}")
            st.sidebar.write(f"Marketplace Symbol: {marketplace_symbol}")
            st.sidebar.write(f"Current Token ID Counter: {token_id_counter}")

        except:
            st.sidebar.write("Unable to fetch marketplace details.")

    # Get NFT listings
    def get_listings():
        if marketplace_contract is None:
            return []
        listings = marketplace_contract.functions.getNFTListings().call()
        return listings


    # Display listings
    def display_listings():
        listings = get_listings()

        if len(listings) == 0:
            st.write("No NFTs Listed.")
        else:
            st.write("Available NFT Listings:")
            for listing in listings:
                st.write(f"Token ID: {listing[0]} | Seller: {listing[1]} | Price: {listing[2]} ETH")
                ipfs_img = ipfs_url + listing[4]  
                st.image(ipfs_img, caption="NFT Image", use_column_width=True)

    # Display NFT listings
    display_listings()

    # WebUI for NFTs
    st.sidebar.write("Add NFT from IPFS:")
    ipfs_hash = st.sidebar.text_input("Enter IPFS Hash / CID")
    price = st.sidebar.number_input("Price (ETH)", min_value=0.10, step=0.10)
    if st.sidebar.button("Add NFT"):
        if st.session_state.contract_address and ipfs_hash and price > 0:
            contract_address = st.session_state.contract_address  
            deployer_account = st.session_state.deployer_address
            marketplace_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

            # Estimate the gas listing NFTs
            estimated_gas = marketplace_contract.functions.createAndListNFT(ipfs_hash, w3.toWei(price, 'ether')).estimateGas({'from': deployer_account})
            
            try:
                tx_hash = marketplace_contract.functions.createAndListNFT(ipfs_hash, w3.toWei(price, 'ether')).transact({
                    'from': deployer_account,
                    'gas': estimated_gas,
                    'gasPrice': w3.eth.gasPrice
                })  

                st.sidebar.write("NFT added and listed successfully!")
                display_listings()

            except Exception as e:
                st.write(f"Error: {e}")


