pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

import "./ERC721Full.sol";
import "./MinterRole.sol";  
import "./Counters.sol";
import "./Roles.sol";

contract NFTMarketplace is ERC721Full, MinterRole {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    struct NFTListing {
        uint256 tokenId;
        address seller;
        uint256 price;
        bool active;
        string ipfsHash;
    }

    mapping(uint256 => NFTListing) public nftListings;

    constructor(string memory _name, string memory _symbol) ERC721Full(_name, _symbol) public {
        if (!isMinter(address(this))) {
            _addMinter(address(this));  
        }
        if (!isMinter(msg.sender)) {
            _addMinter(msg.sender);
        }
    }

    function mintNFT(address to, string memory ipfs_hash) public onlyMinter {
        uint256 tokenId = _tokenIdCounter.current();
        _mint(to, tokenId);
        _setTokenURI(tokenId, ipfs_hash);
        _tokenIdCounter.increment();
    }

    function getTokenIdCounter() public view returns (uint256) {
        return _tokenIdCounter.current();
    }

    function isTokenActive(uint256 tokenId) public view returns (bool) {
        return nftListings[tokenId].active;
    }

    function createAndListNFT(string memory ipfs_hash, uint256 price) public onlyMinter {
        uint256 tokenId = _tokenIdCounter.current();
        _mint(address(this), tokenId);  // Mint the NFT to the contract's address
        _setTokenURI(tokenId, ipfs_hash);  
        _tokenIdCounter.increment();

        require(price > 0, "Price must be greater than 0");
        nftListings[tokenId] = NFTListing(tokenId, address(this), price, true, ipfs_hash);
    }

    function listNFT(uint256 tokenId, uint256 price, string memory ipfs_hash) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved or owner");
        require(price > 0, "Price must be greater than 0");
        require(!_exists(tokenId) || !nftListings[tokenId].active, "NFT already listed");

        nftListings[tokenId] = NFTListing(tokenId, msg.sender, price, true, ipfs_hash);
    }

    function delistNFT(uint256 tokenId) public {
        require(nftListings[tokenId].active, "NFT not listed");
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved or owner");

        delete nftListings[tokenId];
    }

    function buyNFT(uint256 tokenId) public payable {
        NFTListing memory listing = nftListings[tokenId];
        require(listing.active, "NFT not listed");
        require(msg.value >= listing.price, "Insufficient funds sent");
        require(msg.sender != listing.seller, "Cannot buy your own NFT");

        nftListings[tokenId].active = false;
        transferFrom(listing.seller, msg.sender, tokenId);

        address(uint160(listing.seller)).transfer(listing.price);
    }

    function getNFTListings() public view returns (NFTListing[] memory) {
        uint256 numListings = 0;
        for (uint256 i = 0; i < _tokenIdCounter.current(); i++) {
            if (nftListings[i].active) {
                numListings++;
            }
        }

        NFTListing[] memory listings = new NFTListing[](numListings);
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < _tokenIdCounter.current(); i++) {
            if (nftListings[i].active) {
                listings[currentIndex] = nftListings[i];
                currentIndex++;
            }
        }
        return listings;
    }
}
