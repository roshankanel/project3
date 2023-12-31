![The Metavault Marketplace](The_Metavault.PNG)
# Metavault

Welcome to the Metavault project's GitLab repository! This repository contains code and resources related to the exciting world of NFTs, Solidity, Remix, and SolcX. Below, you'll find a brief overview of each of these components and how they contribute to the Metavault project.

## About the Metavault Project

The **Metavault** project is a blockchain-based endeavor that focuses on creating and managing Non-Fungible Tokens (NFTs) using the Ethereum blockchain. NFTs are unique digital assets that have gained significant attention for their ability to represent ownership of digital and physical items, digital art, collectibles, virtual real estate, and more.

## NFTs (Non-Fungible Tokens)

NFTs, or Non-Fungible Tokens, are a type of digital asset that represent ownership or proof of authenticity of a unique item. Unlike cryptocurrencies such as Bitcoin or Ethereum, NFTs are indivisible and cannot be exchanged on a one-to-one basis. Each NFT has its own distinct value and characteristics, making them ideal for representing unique digital creations.

## Solidity

**Solidity** is a high-level programming language specifically designed for writing smart contracts on the Ethereum blockchain. Smart contracts are self-executing contracts with the terms of the agreement directly written into code. In the context of the Metavault project, Solidity is used to create the smart contracts that define the behavior and properties of our NFTs.

## Remix

**Remix** is a powerful and user-friendly integrated development environment (IDE) for writing, testing, and deploying smart contracts on the Ethereum blockchain. It provides a web-based interface that allows developers to interact with their contracts, simulate transactions, and ensure their code functions as intended before deployment. We use Remix to streamline the development and testing process of our Solidity smart contracts. 

## SolcX

**SolcX** is the Solidity compiler that aids in converting human-readable Solidity code into bytecode that can be executed on the Ethereum Virtual Machine (EVM). It helps in transforming the smart contract code into a format that can be understood and executed by the Ethereum network. This compiler is an essential tool in the development and deployment of our NFT-related smart contracts.

## Ganache

**Ganache** is a personal blockchain for Ethereum development that you can use to deploy contracts, develop your applications, and run tests. It provides a local Ethereum blockchain that you can use for development and testing purposes, allowing you to avoid the costs and complexities associated with deploying contracts on the main Ethereum network.

## Getting Started

To get started with the Metavault project, follow these steps:
 1. Install IPFS Desktop
 2. Install Remix Desktop
 3. Install Ganache Desktop
 4. Install all libraries required (detailed in requirements.txt) <br />
        a. If you need to adjust your environment for this or any development project we highly recommend using the following method to take an environment snapshot: <br />
                         "pip freeze > requirements.txt" <br />
        b. This stores your current installed libraries and versions into a requirements.txt file to ensure exact restoration of your development environment in the event of any issues,
           rebuilds or replication requirements. <br />
 6. Ensure all the files here are in your runtime environment, all the .sol files are from the ERC721 standard and dependencies required.
 7. Run your IPFS, Remix and Ganache Desktop apps
 8. Run the python file with "streamlit run *.py"
 9. If uploading NFTs, copy the IPFS (or CID) from the desktop app
 10. Follow the instruction in the streamlit app

## End Product

The Metavault is a fully functional NFT marketplace application which allows the users to deploy the smart contract and to create, purchase and exchange ERC721-standard NFTs with unique images. It is connected with Ganache accounts to be able to demonstrate adn test the functionality of its features. The entire app can be operated using Streamlit.

![Metavault Marketplace](Final_Project_1.png)



