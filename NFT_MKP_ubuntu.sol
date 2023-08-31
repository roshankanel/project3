pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

import "./ERC721Full.sol";
import "./MinterRole.sol";  
import "./Counters.sol";
import "./Roles.sol";
import "./ReentrancyGuard.sol";


contract NFTMarketplace is ERC721Full, MinterRole, ReentrancyGuard {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    address private deployer;

    struct NFTListing {
        uint256 tokenId;
        address seller;
        uint256 price;
        bool active;
        string ipfsHash;
    }

    mapping(uint256 => NFTListing) public nftListings;

    constructor(string memory _name, string memory _symbol) ERC721Full(_name, _symbol) public {
        deployer = msg.sender;
        if (!isMinter(address(this))) {
            _addMinter(address(this));  
        }
        if (!isMinter(msg.sender)) {
            _addMinter(msg.sender);
        }
    }

    function getTokenIdCounter() public view returns (uint256) {
        return _tokenIdCounter.current();
    }
   
    function createAndListNFT(string memory ipfs_hash, uint256 price) public onlyMinter {
        uint256 tokenId = _tokenIdCounter.current();
        require(!_exists(tokenId), "Token already exists");
        _mint(deployer, tokenId); // modified line
        _setTokenURI(tokenId, ipfs_hash);
        _tokenIdCounter.increment();
        require(price > 0, "Price must be greater than 0");
        nftListings[tokenId] = NFTListing(tokenId, deployer, price, true, ipfs_hash);
        emit Listed(tokenId, deployer, price, ipfs_hash);
    }

    function delistNFT(uint256 tokenId) public {
        require(nftListings[tokenId].active, "NFT not listed");
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not approved or owner");

        delete nftListings[tokenId];

        emit Delisted(tokenId, msg.sender);
    }

    function getNFTListings() public view returns (NFTListing[] memory) {
        NFTListing[] memory listings = new NFTListing[](_tokenIdCounter.current());
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < _tokenIdCounter.current(); i++) {
            if (nftListings[i].active) {
                listings[currentIndex] = nftListings[i];
                currentIndex++;
            }
        }
        return listings;
    }
    
    function buyNFT(address payable contract_owner) public payable {
        contract_owner.transfer(msg.value);
    }
}
