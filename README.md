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

[Diamond Louper](https://louper-mark3labs-pro.vercel.app/?address=0x3D234faB36905f4d75753564f3301f2119Cb9cCA&network=kovan) 

DcaDiamond : [0x4e551ab784a1acDDE29eb4A5C4c6275d8fA4D52D](https://kovan.etherscan.io/address/0x4e551ab784a1acDDE29eb4A5C4c6275d8fA4D52D) \
DiamondCutFacet : [0x9d748B2d70138F6695D2285a2cBe354b13E2F1C9](https://kovan.etherscan.io/address/0x9d748B2d70138F6695D2285a2cBe354b13E2F1C9) \
DiamondLoupeFacet : [0x94beDd10b9E22870EF8F5a68dc1bA4b006577797](https://kovan.etherscan.io/address/0x94beDd10b9E22870EF8F5a68dc1bA4b006577797) \
OwnershipFacet : [0x1e201Ce87c8392704a5FfCD6E163380896CD3921](https://kovan.etherscan.io/address/0x1e201Ce87c8392704a5FfCD6E163380896CD3921) \
DcaManagerFacet : [0xBbb3CC5B56C450DF2A22b740A3652975c45ef021](https://kovan.etherscan.io/address/0xBbb3CC5B56C450DF2A22b740A3652975c45ef021) \
DcaKeeperFacer : [0xf47911C871472Fb7C5596Fd4DaE93729f8766453](https://kovan.etherscan.io/address/0xf47911C871472Fb7C5596Fd4DaE93729f8766453)

[Keeper](https://keepers.chain.link/kovan/3482) \
[Keeper Test](https://keepers.chain.link/kovan/3463)


