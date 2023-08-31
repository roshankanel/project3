pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract TheMetavault is ERC721Full {
    uint256 public tokenId ;
    constructor() public ERC721Full("TheMetavault", "MTV") {}

    struct Metavault {
        string name;
        uint256 registrationValue;
        string artJson;
    }

    mapping(uint256 => Metavault) public NFTCollection;

    event registration(uint256 tokenId, uint256 registrationValue, string reportURI, string artJson);
    
    function imageUri() public view returns (string memory imageJson){
        return NFTCollection[tokenId].artJson;
    }

    function BalanceCheck(address  account_address) view public returns (uint256) {
        return account_address.balance ;
    }

    function createNFT(address owner, string memory name, uint256 Value, string memory tokenURI, string memory tokenJSON) public returns (uint256) {
        tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        NFTCollection[tokenId] = Metavault(name, Value, tokenJSON);

        emit registration(tokenId, Value, tokenURI, tokenJSON);

        return tokenId;
    }

    function valueCheck(uint256 token_id) view public returns (uint256) {
        // require(_exists(NFTCollection[token_id]),"Token Id does not exist");
        return NFTCollection[token_id].registrationValue ;
        
    }


    function buyNFT(address payable contract_owner) public payable {
        contract_owner.transfer(msg.value);
    }


}
