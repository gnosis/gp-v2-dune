import "@nomiclabs/hardhat-ethers";

import ERC20 from "@openzeppelin/contracts/build/contracts/ERC20.json";
import { BigNumber, Bytes, BytesLike, Contract, utils } from "ethers";
import { HardhatRuntimeEnvironment } from "hardhat/types";

export interface TokenDetails {
  contract: Contract;
  symbol: string | null;
  decimals: number | null;
  address: string;
}

function stripZerosRight(bytes: BytesLike): Bytes {
  return utils.stripZeros(utils.arrayify(bytes).reverse()).reverse();
}

const ERC20_BYTES32_SYMBOL_ABI = `[{
  "inputs": [],
  "name": "symbol",
  "outputs": [{
      "name": "",
      "type": "bytes32"
  }],
  "stateMutability": "view",
  "type": "function"
}]`;

export async function tokenDetails(
  address: string,
  hre: HardhatRuntimeEnvironment,
): Promise<TokenDetails> {
  const contract = new Contract(address, ERC20.abi, hre.ethers.provider);
  const [symbol, decimals] = await Promise.all([
    contract
      .symbol()
      .catch(async () => {
        const bytes32Contract = new Contract(
          address,
          ERC20_BYTES32_SYMBOL_ABI,
          hre.ethers.provider,
        );
        return utils.toUtf8String(
          stripZerosRight(await bytes32Contract.symbol()),
        );
      })
      .catch(() => null),
    contract
      .decimals()
      .then((s: unknown) => BigNumber.from(s))
      .catch(() => null),
  ]);
  return {
    contract,
    symbol,
    decimals,
    address,
  };
}
