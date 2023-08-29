import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time
import base64

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()


# Initialize variables

NFT_listings = []

NFT_collection = {}

token_ids = []


if "NFT_collection" not in st.session_state:
             st.session_state['NFT_collection'] = NFT_collection

if "NFT_listings" not in st.session_state:
             st.session_state['NFT_listings'] = NFT_listings

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Load_Contract Function
################################################################################


# @st.cache(allow_output_mutation=True)
@st.cache_resource



def get_base64_of_bin_file2(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file2(png_file) 
    page_bg_img = '''
    <style>
    .stApp {

    background-image: url("data:image/png;base64,%s");
    background-position: center;
    background-size: 2200px 1400px;

    background-repeat: no-repeat;
    background-attachment: scroll; # doesn't work

    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def load_contract():

    # Load the contract ABI
    with open(Path('./Metavault_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_NFT(NFT_name, NFT_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(NFT_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": NFT_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


# WebUI for pages
menu = ["Deploy Marketplace Contract", "Marketplace", "Exchange"]
choice = st.sidebar.selectbox("Select an option", menu)


# Deploty Contract Page
if choice == "Deploy Marketplace Contract":

    set_png_as_page_bg('The_Metavault.PNG')

    st.markdown("# :red[The Metavault]")
    st.sidebar.markdown("## NFT Marketplace Deployment & Purchasing")

    st.sidebar.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = st.sidebar.selectbox("Select Account", options=accounts)
    st.sidebar.markdown("---")



# Marketplace Page
if choice == "Marketplace":

    set_png_as_page_bg('The_Metavault.PNG')

    st.markdown("# :red[The Metavault]")
    st.sidebar.markdown("## NFT Marketplace Deployment & Purchasing")

    st.sidebar.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = st.sidebar.selectbox("Select Account", options=accounts)
    st.sidebar.markdown("---")

    ################################################################################
    # Register New Artwork
    ################################################################################


    st.sidebar.markdown("## Register New NFT")
    NFT_name = st.sidebar.text_input("Enter the name of the NFT")
    value = st.sidebar.text_input("Enter the value of the NFT")

    # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
    file = st.sidebar.file_uploader("Upload NFT", type=["jpg", "jpeg", "png"])

    # NFT_listings = {}

    register_NFT = st.sidebar.button("Register NFT")


    st.sidebar.markdown("---")

    # Reset values to state before rreun
    NFT_collection = st.session_state['NFT_collection']
    NFT_listings = st.session_state['NFT_listings']


    if register_NFT:

        # Use the `pin_artwork` helper function to pin the file to IPFS
        NFT_ipfs_hash, token_json = pin_NFT(NFT_name, file)

        artwork_uri = f"ipfs://{NFT_ipfs_hash}"

        tx_hash = contract.functions.createNFT(
            address,
            NFT_name,
            # artist_name,
            int(value),
            artwork_uri,
            token_json['image']
        # ).transact({'from': address, 'gas': 1000000})
        ).transact({'from': address, 'gas': 10000000})   
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("NFT Succcessfully Created")     

        NFT_token_id = contract.functions.tokenId().call()
        appraisal_filter = contract.events.Appraisal.createFilter(fromBlock=0, argument_filters={"tokenId": NFT_token_id})
        reports = appraisal_filter.get_all_entries()

        for report in reports:

            report_dictionary = dict(report)
            
            image_uri = report_dictionary["args"]["artJson"]
    # 
            # st.image(f'https://ipfs.io/ipfs/{image_uri}') 

            image_url = 'https://ipfs.io/ipfs/' + image_uri

            NFT_collection[report_dictionary["args"]["tokenId"]] = image_url

            list = (report_dictionary["args"]["tokenId"],NFT_name,value)
            NFT_listings.append(list)

            # Store values in session state
            st.session_state['NFT_collection'] = NFT_collection
            st.session_state['NFT_listings'] = NFT_listings



    # Deploy NFTs

    # st.sidebar.markdown("## Deploy to The Metavault")
    # deploy_NFT = st.sidebar.button("Deploy NFT Collection")

    # if deploy_NFT:

    #     values = list(NFT_collection.items())
    #     for i in range(len(NFT_collection)):
    #         st.image(values[i][1], width=400)
    #         st.write(f'Token Id: {NFT_listings[i][0]}, Name :  {NFT_listings[i][1]}, Value: {NFT_listings[i][2]}')
    #         # st.write(NFT_collection[i])


    # View Listings

    if st.button('View Listings'):
        values = list(NFT_collection.items())
        for i in range(len(NFT_collection)):
            st.image(values[i][1], width=400)
            st.write(f'Token Id: {NFT_listings[i][0]}, Name :  {NFT_listings[i][1]}, Value: {NFT_listings[i][2]}')


    for i in range(len(NFT_collection)):
         token_ids.append(NFT_listings[i][0])


    st.session_state['token_ids'] = token_ids


    # Purchase NFT

    st.sidebar.markdown("## Purchase NFT")

    buyer_address = st.sidebar.selectbox("Select Your Account Address", options=accounts)
    selected_NFT = st.sidebar.selectbox("Select the NFT Id You Would Like to Purcahse", options=token_ids)


    pruchase_NFT = st.sidebar.button("Purchase NFT")


    if pruchase_NFT:

        purchase_tx_hash = contract.functions.safeTransferFrom(
            address,
            buyer_address,
            selected_NFT
        # ).transact({'from': address, 'gas': 1000000})
        ).transact({'from': address, 'gas': 10000000})   
        
        if purchase_tx_hash:
            # st.sidebar.write(f'purchase_tx_hash : {purchase_tx_hash}')
            st.write(f'NFT with Id {selected_NFT} has been purchased by account address {buyer_address}')     



# Exchange Page
elif choice == "Exchange":

    set_png_as_page_bg('The_Metavault.png')

    accounts = w3.eth.accounts

    st.markdown("# :red[The Metavault]")
    st.sidebar.markdown("## NFT Exchange")


    # Reset values to state before rreun
    NFT_listings = st.session_state['NFT_listings']
    NFT_collection = st.session_state['NFT_collection']
    token_ids = st.session_state['token_ids']


    if st.button('View Listings'):
        values = list(NFT_collection.items())
        for i in range(len(NFT_collection)):
            st.image(values[i][1], width=400)
            st.write(f'Token Id: {NFT_listings[i][0]}, Name :  {NFT_listings[i][1]}, Value: {NFT_listings[i][2]}')


    # NFT Owner Check
    # st.sidebar.markdown("## Find NFT Holder")
    
    # owned_NFT = st.sidebar.selectbox("Select the NFT Id You Would Like to find the owner of", options=token_ids)
    # owner_NFT = st.sidebar.button("OwnerOf")

    # if owner_NFT:

    #     new_owner = contract.functions.ownerOf(owned_NFT).call()
    #     # ).transact({'from': address, 'gas': 1000000})
    #     st.sidebar.write(f'NFT with Id {owned_NFT} is owned by account address {new_owner}')     
    


    # View Accounts' NFTs

    st.sidebar.markdown("## View Account Vaults")

    view_address = st.sidebar.selectbox("Select the Account Address", options=accounts)


    view_NFT = st.sidebar.button("View Account's Vault")

    st.sidebar.markdown("---")

    held_NFTs = []

    if view_NFT:
          for NFTs in range(len(token_ids)):
               if contract.functions.ownerOf(token_ids[NFTs]).call() == view_address:
                    held_NFTs.append(token_ids[NFTs])
          if len(held_NFTs) == 0:
               st.write(f'Owner of account {view_address} does not hold any NFTs')
          else:
               st.write(f'Owner of account {view_address} holds NFT with Id: {held_NFTs}')
        #   st.write(NFT_collection)
        #   st.image

          for i in range(len(held_NFTs)):
            st.image(NFT_collection[held_NFTs[i]], width=400)

            for nfts in range(len(token_ids)): 
                if held_NFTs[i] == NFT_listings[nfts][0]: 
                    st.write(NFT_listings[nfts])



    # Exhchange NFT

    st.sidebar.markdown("## Exchange NFTs")

    from_address = st.sidebar.selectbox("Select Exchange From Account Address", options=accounts)
    to_address = st.sidebar.selectbox("Select Exchange To Account Address", options=accounts)
    selected_NFT = st.sidebar.selectbox("Select the NFT Id You Would Like to Exchange", options=token_ids)



    Exchange_NFT = st.sidebar.button("## Exchange NFT")


    if Exchange_NFT:

        purchase_tx_hash = contract.functions.safeTransferFrom(
            from_address,
            to_address,
            selected_NFT
        # ).transact({'from': address, 'gas': 1000000})
        ).transact({'from': from_address, 'gas': 10000000})   
        # st.sidebar.write(f'purchase_tx_hash : {purchase_tx_hash}')
        st.write(f'NFT with Id {selected_NFT} has been exchanged from {from_address} to {to_address}')     



