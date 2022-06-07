[![dca-dao](https://circleci.com/gh/dca-dao/smart-contracts.svg?style=svg)](https://app.circleci.com/pipelines/gh/dca-dao/smart-contracts)

# Smart contract
Smart contracts for our dApp  
For more info, check this [README](https://github.com/dca-dao/.github/blob/master/profile/README.md)
# Planning
- 15/02 : autoformation Solidity et web3
- 21/02 : initialisation du projet et recherche de Keeper sur Avalanche
- 22/02 : projet test intégration avec Aaave
- 28/02 : création contract avec function pour fund et withdraw
- 01/03 : test unitaire fund et withdraw + recherche proxy
- 14/03 : réflexion sur l'architecture de l'application et sur l'automatisation avec [Gelato](https://www.gelato.network/)
- 04/04 : recherche sur intégration AMM avec Uniswap et intégration simple swap
- 05/04 : appel router UniswapV3 + transfer WETH + recherche sur Aave + recherche d'une plateforme de staking sur le testnet eth
- 12/04 : recherche sur le lending Aave sur le testnet + interactions avec le [contrat](https://github.com/aave/aave-v3-core/blob/master/contracts/protocol/pool/Pool.sol) et Déployer SwapRouter test sur Roptsen + test sur etherscan
- 28/05 : création du [Keeper](https://keepers.chain.link/kovan/3404)
- 30/05 : méthode fund et withdraw sur DcaManager et gestion des DcaSettings
- 31/05 : implémentation diamond patern
- 06/06 : implémentation d'un contrat pour gérer l'ensemble des comptes des utilisateurs ainsi que la configuration de leur DCA
- 07/06 : test unitaire sur DcaManager et DcaKeeper

[Diamond Louper](https://louper-mark3labs-pro.vercel.app/?address=0xe76B1F8e12d6491639c798B58De0b49F9b3b6ce2&network=kovan) 

DcaDiamond : [0x4e551ab784a1acDDE29eb4A5C4c6275d8fA4D52D](https://kovan.etherscan.io/address/0x4e551ab784a1acDDE29eb4A5C4c6275d8fA4D52D) \
DiamondCutFacet : [0xb3c6EF2BC56De7A14f29De34399fBDBFF25eBEB4](https://kovan.etherscan.io/address/0xb3c6EF2BC56De7A14f29De34399fBDBFF25eBEB4) \
DiamondLoupeFacet : [0x029943bE770a657EE81dbDc36beB86937565092C](https://kovan.etherscan.io/address/0x029943bE770a657EE81dbDc36beB86937565092C) \
OwnershipFacet : [0x96fB440Cd507D741BA852c34B15FF9Cb4e395B15](https://kovan.etherscan.io/address/0x96fB440Cd507D741BA852c34B15FF9Cb4e395B15) \
DcaManagerFacet : [0x0aD9E091755fE045ab0Aaf4da1925Ce68AE7F9e6](https://kovan.etherscan.io/address/0x0aD9E091755fE045ab0Aaf4da1925Ce68AE7F9e6) \
DcaKeeperFacer : [0xeD40A5D893DA6F2fE080A07770f132B969Ff2285](https://kovan.etherscan.io/address/0xeD40A5D893DA6F2fE080A07770f132B969Ff2285)

[Keeper](https://keepers.chain.link/kovan/3483) \
[Keeper Test](https://keepers.chain.link/kovan/3463)


