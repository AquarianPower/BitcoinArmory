################################################################################
#                                                                              #
# Copyright (C) 2011-2014, Armory Technologies, Inc.                           #
# Distributed under the GNU Affero General Public License (AGPL v3)            #
# See LICENSE or http://www.gnu.org/licenses/agpl.html                         #
#                                                                              #
################################################################################

import sys
sys.path.append('..')
import unittest
import sys
sys.path.append('..')
import textwrap

from armoryengine.ArmoryUtils import *
from armoryengine.ArmoryEncryption import *
from armoryengine.WalletEntry import *
from armoryengine.ArmoryKeyPair import *

WALLET_VERSION_BIN = hex_to_binary('002d3101')

# This disables RSEC for all WalletEntry objects.  This causes it to stop
# checking RSEC codes on all entries, and writes all \x00 bytes when creating.
WalletEntry.DisableRSEC()


MSO_FILECODE   = 'MOCKOBJ_'
MSO_ENTRY_ID   = '\x01'+'\x33'*20
MSO_FLAGS_REG  = '\x00\x00'
MSO_FLAGS_DEL  = '\x80\x00'
MSO_PARSCRADDR = '\x05'+'\x11'*20
MSO_PAYLOAD    = '\xaf'*5

FAKE_KDF_ID  = '\x42'*8
FAKE_EKEY_ID = '\x9e'*8



BIP32TestVectors = []

# 0
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35")),
      'seedCC': SecureBinaryData(hex_to_binary("873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508")),
      'seedPubKey': SecureBinaryData(hex_to_binary("0439a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c23cbe7ded0e7ce6a594896b8f62888fdbc5c8821305e2ea42bf01e37300116281")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade4000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d50800e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d5080339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2")),
      'seedID': SecureBinaryData(hex_to_binary("3442193e1bb70916e914552172cd4e2dbc9df811")),
      'seedFP': SecureBinaryData(hex_to_binary("3442193e")),
      'seedParFP': SecureBinaryData(hex_to_binary("00000000")),
      'nextChild': 2147483648 
   })

# 1
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("00edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea")),
      'seedCC': SecureBinaryData(hex_to_binary("47fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae6236141")),
      'seedPubKey': SecureBinaryData(hex_to_binary("045a784662a4a20a65bf6aab9ae98a6c068a81c52e4b032c0fb5400c706cfccc567f717885be239daadce76b568958305183ad616ff74ed4dc219a74c26d35f839")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("035a784662a4a20a65bf6aab9ae98a6c068a81c52e4b032c0fb5400c706cfccc56")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade4013442193e8000000047fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae623614100edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e013442193e8000000047fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae6236141035a784662a4a20a65bf6aab9ae98a6c068a81c52e4b032c0fb5400c706cfccc56")),
      'seedID': SecureBinaryData(hex_to_binary("5c1bd648ed23aa5fd50ba52b2457c11e9e80a6a7")),
      'seedFP': SecureBinaryData(hex_to_binary("5c1bd648")),
      'seedParFP': SecureBinaryData(hex_to_binary("3442193e")),
      'nextChild': 1
   })

# 2
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("003c6cb8d0f6a264c91ea8b5030fadaa8e538b020f0a387421a12de9319dc93368")),
      'seedCC': SecureBinaryData(hex_to_binary("2a7857631386ba23dacac34180dd1983734e444fdbf774041578e9b6adb37c19")),
      'seedPubKey': SecureBinaryData(hex_to_binary("04501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c008794c1df8131b9ad1e1359965b3f3ee2feef0866be693729772be14be881ab")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("03501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade4025c1bd648000000012a7857631386ba23dacac34180dd1983734e444fdbf774041578e9b6adb37c19003c6cb8d0f6a264c91ea8b5030fadaa8e538b020f0a387421a12de9319dc93368")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e025c1bd648000000012a7857631386ba23dacac34180dd1983734e444fdbf774041578e9b6adb37c1903501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c")),
      'seedID': SecureBinaryData(hex_to_binary("bef5a2f9a56a94aab12459f72ad9cf8cf19c7bbe")),
      'seedFP': SecureBinaryData(hex_to_binary("bef5a2f9")),
      'seedParFP': SecureBinaryData(hex_to_binary("5c1bd648")),
      'nextChild': 2147483650
   })

# 3
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("00cbce0d719ecf7431d88e6a89fa1483e02e35092af60c042b1df2ff59fa424dca")),
      'seedCC': SecureBinaryData(hex_to_binary("04466b9cc8e161e966409ca52986c584f07e9dc81f735db683c3ff6ec7b1503f")),
      'seedPubKey': SecureBinaryData(hex_to_binary("0457bfe1e341d01c69fe5654309956cbea516822fba8a601743a012a7896ee8dc24310ef3676384179e713be3115e93f34ac9a3933f6367aeb3081527ea74027b7")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("0357bfe1e341d01c69fe5654309956cbea516822fba8a601743a012a7896ee8dc2")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade403bef5a2f98000000204466b9cc8e161e966409ca52986c584f07e9dc81f735db683c3ff6ec7b1503f00cbce0d719ecf7431d88e6a89fa1483e02e35092af60c042b1df2ff59fa424dca")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e03bef5a2f98000000204466b9cc8e161e966409ca52986c584f07e9dc81f735db683c3ff6ec7b1503f0357bfe1e341d01c69fe5654309956cbea516822fba8a601743a012a7896ee8dc2")),
      'seedID': SecureBinaryData(hex_to_binary("ee7ab90cde56a8c0e2bb086ac49748b8db9dce72")),
      'seedFP': SecureBinaryData(hex_to_binary("ee7ab90c")),
      'seedParFP': SecureBinaryData(hex_to_binary("bef5a2f9")),
      'nextChild': 2
   })

# 4
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("000f479245fb19a38a1954c5c7c0ebab2f9bdfd96a17563ef28a6a4b1a2a764ef4")),
      'seedCC': SecureBinaryData(hex_to_binary("cfb71883f01676f587d023cc53a35bc7f88f724b1f8c2892ac1275ac822a3edd")),
      'seedPubKey': SecureBinaryData(hex_to_binary("04e8445082a72f29b75ca48748a914df60622a609cacfce8ed0e35804560741d292728ad8d58a140050c1016e21f285636a580f4d2711b7fac3957a594ddf416a0")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("02e8445082a72f29b75ca48748a914df60622a609cacfce8ed0e35804560741d29")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade404ee7ab90c00000002cfb71883f01676f587d023cc53a35bc7f88f724b1f8c2892ac1275ac822a3edd000f479245fb19a38a1954c5c7c0ebab2f9bdfd96a17563ef28a6a4b1a2a764ef4")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e04ee7ab90c00000002cfb71883f01676f587d023cc53a35bc7f88f724b1f8c2892ac1275ac822a3edd02e8445082a72f29b75ca48748a914df60622a609cacfce8ed0e35804560741d29")),
      'seedID': SecureBinaryData(hex_to_binary("d880d7d893848509a62d8fb74e32148dac68412f")),
      'seedFP': SecureBinaryData(hex_to_binary("d880d7d8")),
      'seedParFP': SecureBinaryData(hex_to_binary("ee7ab90c")),
      'nextChild': 1000000000
   })

# 5
BIP32TestVectors.append( \
   {
      'seedKey': SecureBinaryData(hex_to_binary("00471b76e389e528d6de6d816857e012c5455051cad6660850e58372a6c3e6e7c8")),
      'seedCC': SecureBinaryData(hex_to_binary("c783e67b921d2beb8f6b389cc646d7263b4145701dadd2161548a8b078e65e9e")),
      'seedPubKey': SecureBinaryData(hex_to_binary("042a471424da5e657499d1ff51cb43c47481a03b1e77f951fe64cec9f5a48f7011cf31cb47de7ccf6196d3a580d055837de7aa374e28c6c8a263e7b4512ceee362")),
      'seedCompPubKey': SecureBinaryData(hex_to_binary("022a471424da5e657499d1ff51cb43c47481a03b1e77f951fe64cec9f5a48f7011")),
      'seedExtSerPrv': SecureBinaryData(hex_to_binary("0488ade405d880d7d83b9aca00c783e67b921d2beb8f6b389cc646d7263b4145701dadd2161548a8b078e65e9e00471b76e389e528d6de6d816857e012c5455051cad6660850e58372a6c3e6e7c8")),
      'seedExtSerPub': SecureBinaryData(hex_to_binary("0488b21e05d880d7d83b9aca00c783e67b921d2beb8f6b389cc646d7263b4145701dadd2161548a8b078e65e9e022a471424da5e657499d1ff51cb43c47481a03b1e77f951fe64cec9f5a48f7011")),
      'seedID': SecureBinaryData(hex_to_binary("d69aa102255fed74378278c7812701ea641fdf32")),
      'seedFP': SecureBinaryData(hex_to_binary("d69aa102")),
      'seedParFP': SecureBinaryData(hex_to_binary("d880d7d8")),
      'nextChild': None
   })



SEEDTEST = [{}, {}]

SEEDTEST[0]['Seed']  = SecureBinaryData(hex_to_binary("000102030405060708090a0b0c0d0e0f"));
SEEDTEST[0]['Priv']  = SecureBinaryData(hex_to_binary("e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"));
SEEDTEST[0]['Pubk']  = SecureBinaryData(hex_to_binary("0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2"));
SEEDTEST[0]['Chain'] = SecureBinaryData(hex_to_binary("873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508"));

SEEDTEST[1]['Seed']  = SecureBinaryData(hex_to_binary("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542"));
SEEDTEST[1]['Priv']  = SecureBinaryData(hex_to_binary("4b03d6fc340455b363f51020ad3ecca4f0850280cf436c70c727923f6db46c3e"));
SEEDTEST[1]['Pubk']  = SecureBinaryData(hex_to_binary("03cbcaa9c98c877a26977d00825c956a238e8dddfbd322cce4f74b0b5bd6ace4a7"));
SEEDTEST[1]['Chain'] = SecureBinaryData(hex_to_binary("60499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd9689"));




################################################################################
class MockWalletFile(object):
   def __init__(self):
      self.ekeyMap = {}

   def doFileOperation(*args, **kwargs):
      pass

   def addFileOperationToQueue(*args, **kwargs):
      pass

   def fsyncUpdates(*args, **kwargs):
      pass

   def getName(self):
      return 'MockWalletFile'



################################################################################
def skipFlagExists():
   if os.path.exists('skipmosttests.flag'):
      print '*'*80
      print 'SKIPPING MOST TESTS.  REMOVE skipMostTests.flag TO REENABLE'
      print '*'*80
      return True
   else:
      return False


################################################################################
class UtilityFuncTests(unittest.TestCase):

   #############################################################################
   def testSplitChildIndex(self):
      self.assertRaises(ValueError, SplitChildIndex, 2**32)
      self.assertRaises(ValueError, SplitChildIndex, -1)

      TOPBIT = HARDBIT
      self.assertEqual(SplitChildIndex(0),          [0, False])
      self.assertEqual(SplitChildIndex(1),          [1, False])
      self.assertEqual(SplitChildIndex(128),        [128, False])
      self.assertEqual(SplitChildIndex(0+TOPBIT),   [0, True])
      self.assertEqual(SplitChildIndex(1+TOPBIT),   [1, True])
      self.assertEqual(SplitChildIndex(2**32-1),    [2**31-1, True])
      self.assertEqual(SplitChildIndex(0x7fffffff), [0x7fffffff, False])
      self.assertEqual(SplitChildIndex(HARDBIT), [0, True])


   #############################################################################
   def testCreateChildIndex(self):
      TOPBIT = HARDBIT
      self.assertEqual(CreateChildIndex(0, False),          0)
      self.assertEqual(CreateChildIndex(1, False),          1)
      self.assertEqual(CreateChildIndex(128, False),        128)
      self.assertEqual(CreateChildIndex(0, True),           0+TOPBIT)
      self.assertEqual(CreateChildIndex(1, True),           1+TOPBIT)
      self.assertEqual(CreateChildIndex(2**31-1, True),     2**32-1)
      self.assertEqual(CreateChildIndex(0x7fffffff, False), 0x7fffffff)
      self.assertEqual(CreateChildIndex(0, True),           HARDBIT)

   #############################################################################
   def testChildIdxToStr(self):
      TOPBIT = HARDBIT
      self.assertEqual(ChildIndexToStr(0), "0")
      self.assertEqual(ChildIndexToStr(1), "1")
      self.assertEqual(ChildIndexToStr(128), "128")
      self.assertEqual(ChildIndexToStr(0+TOPBIT), "0'")
      self.assertEqual(ChildIndexToStr(1+TOPBIT), "1'")
      self.assertEqual(ChildIndexToStr(2**32-1), "2147483647'")
      self.assertEqual(ChildIndexToStr(0x7fffffff), "2147483647")
      self.assertEqual(ChildIndexToStr(HARDBIT), "0'")




################################################################################
class TestHDWalletLogic(unittest.TestCase):

   #############################################################################
   def testCppConvertSeed(self):
      extkey = Cpp.HDWalletCrypto().ConvertSeedToMasterKey(SEEDTEST[0]['Seed'])
      self.assertEqual(extkey.getPrivateKey(), SEEDTEST[0]['Priv'])
      self.assertEqual(extkey.getPublicKey(), SEEDTEST[0]['Pubk'])
      self.assertEqual(extkey.getChaincode(), SEEDTEST[0]['Chain'])
      
      extkey = Cpp.HDWalletCrypto().ConvertSeedToMasterKey(SEEDTEST[1]['Seed'])
      self.assertEqual(extkey.getPrivateKey(), SEEDTEST[1]['Priv'])
      self.assertEqual(extkey.getPublicKey(), SEEDTEST[1]['Pubk'])
      self.assertEqual(extkey.getChaincode(), SEEDTEST[1]['Chain'])


   #############################################################################
   def testCppDeriveChild(self):

      for i in range(len(BIP32TestVectors)-1):
         currEKdata = BIP32TestVectors[i]
         nextEKdata = BIP32TestVectors[i+1]


         currEK = Cpp.ExtendedKey(currEKdata['seedKey'], currEKdata['seedCC'])
         compEK = Cpp.HDWalletCrypto().childKeyDeriv(currEK, currEKdata['nextChild'])
         nextPriv = SecureBinaryData(nextEKdata['seedKey'].toBinStr()[1:])
         self.assertEqual(compEK.getPrivateKey(), nextPriv)
         self.assertEqual(compEK.getPublicKey(), nextEKdata['seedCompPubKey'])
         self.assertEqual(compEK.getChaincode(), nextEKdata['seedCC'])

         if currEKdata['nextChild'] & HARDBIT == 0:
            # Now test the same thing from the just the public key
            currEK = Cpp.ExtendedKey(currEKdata['seedCompPubKey'], currEKdata['seedCC'])
            compEK = Cpp.HDWalletCrypto().childKeyDeriv(currEK, currEKdata['nextChild'])
            #self.assertTrue(currEK.isPub())
            #self.assertEqual(compEK.getPublicKey(), nextEKdata['seedCompPubKey'])
            #self.assertEqual(compEK.getChaincode(), nextEKdata['seedCC'])
         
         

################################################################################
################################################################################
#
# Armory BIP32 Extended Key tests (NO ENCRYPTION)
#
################################################################################
################################################################################

################################################################################
class ABEK_NoCrypt_Tests(unittest.TestCase):

   #############################################################################
   def setUp(self):
      pass
      
   #############################################################################
   def tearDown(self):
      pass
      

   #############################################################################
   def testInitABEK(self):
      #leaf = makeABEKGenericClass()
      abek = ABEK_Generic()
         
      self.assertEqual(abek.isWatchOnly, False)
      self.assertEqual(abek.sbdPrivKeyData, NULLSBD())
      self.assertEqual(abek.sbdPublicKey33, NULLSBD())
      self.assertEqual(abek.sbdChaincode, NULLSBD())
      self.assertEqual(abek.useCompressPub, True)
      self.assertEqual(abek.isUsed, False)
      self.assertEqual(abek.keyBornTime, 0)
      self.assertEqual(abek.keyBornBlock, 0)
      self.assertEqual(abek.privKeyNextUnlock, False)
      self.assertEqual(abek.akpParScrAddr, '')
      self.assertEqual(abek.childIndex, UINT32_MAX)
      self.assertEqual(abek.childPoolSize, 5)
      self.assertEqual(abek.maxChildren, UINT32_MAX)
      self.assertEqual(abek.rawScript, None)
      self.assertEqual(abek.scrAddrStr, None)
      self.assertEqual(abek.uniqueIDBin, None)
      self.assertEqual(abek.uniqueIDB58, None)
      self.assertEqual(abek.akpChildByIndex, {})
      self.assertEqual(abek.akpChildByScrAddr, {})
      self.assertEqual(abek.lowestUnusedChild, 0)
      self.assertEqual(abek.nextChildToCalc,   0)
      self.assertEqual(abek.akpParentRef, None)
      self.assertEqual(abek.masterEkeyRef, None)

      self.assertEqual(abek.TREELEAF, False)
      self.assertEqual(abek.getName(), 'ABEK_Generic')
      self.assertEqual(abek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Uninit)

      # WalletEntry fields
      self.assertEqual(abek.wltFileRef, None)
      self.assertEqual(abek.wltByteLoc, None)
      self.assertEqual(abek.wltEntrySz, None)
      self.assertEqual(abek.isRequired, False)
      self.assertEqual(abek.parEntryID, None)
      self.assertEqual(abek.outerCrypt.serialize(), NULLCRYPTINFO().serialize())
      self.assertEqual(abek.serPayload, None)
      self.assertEqual(abek.defaultPad, 256)
      self.assertEqual(abek.wltParentRef, None)
      self.assertEqual(abek.wltChildRefs, [])
      self.assertEqual(abek.outerEkeyRef, None)
      self.assertEqual(abek.isOpaque,        False)
      self.assertEqual(abek.isUnrecognized,  False)
      self.assertEqual(abek.isUnrecoverable, False)
      self.assertEqual(abek.isDeleted,       False)
      self.assertEqual(abek.isDisabled,      False)
      self.assertEqual(abek.needFsync,       False)

   #############################################################################
   def testSpawnABEK(self):
      sbdPriv  = SecureBinaryData(BIP32TestVectors[1]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[1]['seedCompPubKey']
      sbdChain = BIP32TestVectors[1]['seedCC']
      nextIdx  = BIP32TestVectors[1]['nextChild']

      parA160    = hash160(sbdPubk.toBinStr())
      parScript  = hash160_to_p2pkhash_script(parA160)
      parScrAddr = SCRADDR_P2PKH_BYTE + parA160

      nextPriv  = SecureBinaryData(BIP32TestVectors[2]['seedKey'].toBinStr()[1:])
      nextPubk  = BIP32TestVectors[2]['seedCompPubKey']
      nextChain = BIP32TestVectors[2]['seedCC']

      chA160    = hash160(nextPubk.toBinStr())
      chScript  = hash160_to_p2pkhash_script(chA160)
      chScrAddr = SCRADDR_P2PKH_BYTE + chA160


      abek = ABEK_Generic()
      abek.isWatchOnly = False
      abek.sbdPrivKeyData = sbdPriv.copy()
      abek.sbdPublicKey33 = sbdPubk.copy()
      abek.sbdChaincode   = sbdChain.copy()
      abek.useCompressPub = True
      abek.privKeyNextUnlock = False

      childAbek = abek.spawnChild(nextIdx, fsync=False)

      self.assertEqual(childAbek.sbdPrivKeyData, nextPriv)
      self.assertEqual(childAbek.sbdPublicKey33, nextPubk)
      self.assertEqual(childAbek.sbdChaincode,   nextChain)
      self.assertEqual(childAbek.useCompressPub, True)
      self.assertEqual(childAbek.isUsed, False)
      self.assertEqual(childAbek.privKeyNextUnlock, False)
      self.assertEqual(childAbek.akpParScrAddr, None)
      self.assertEqual(childAbek.childIndex, nextIdx)
      self.assertEqual(childAbek.childPoolSize, 5)
      self.assertEqual(childAbek.maxChildren, UINT32_MAX)
      self.assertEqual(childAbek.rawScript, chScript)
      self.assertEqual(childAbek.scrAddrStr, chScrAddr)
      #self.assertEqual(childAbek.akpChildByIndex, {})
      #self.assertEqual(childAbek.akpChildByScrAddr, {})
      self.assertEqual(childAbek.lowestUnusedChild, 0)
      self.assertEqual(childAbek.nextChildToCalc,   0)
      self.assertEqual(childAbek.akpParentRef, None)
      self.assertEqual(childAbek.masterEkeyRef, None)
      
      # Check the uniqueID, by spawning another child
      subCh = childAbek.spawnChild(0x7fffffff, fsync=False, forIDCompute=True)
      ch256  = hash256(subCh.getScrAddr())
      firstByte = binary_to_int(ch256[0])
      newFirst  = firstByte ^ binary_to_int(ADDRBYTE)
      uidBin = int_to_binary(newFirst) + ch256[1:6]
      uidB58 = binary_to_base58(uidBin)
      self.assertEqual(childAbek.uniqueIDBin, uidBin)
      self.assertEqual(childAbek.uniqueIDB58, uidB58)



   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testSpawnABEK_WO(self):
      #This test appears to demonstrate a problem with pubkey-based spawnChild
      #Disabled for now...

      sbdPriv  = SecureBinaryData(BIP32TestVectors[1]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[1]['seedCompPubKey']
      sbdChain = BIP32TestVectors[1]['seedCC']
      nextIdx  = BIP32TestVectors[1]['nextChild']

      parA160    = hash160(sbdPubk.toBinStr())
      parScript  = hash160_to_p2pkhash_script(parA160)
      parScrAddr = SCRADDR_P2PKH_BYTE + parA160

      nextPriv  = SecureBinaryData(BIP32TestVectors[2]['seedKey'].toBinStr()[1:])
      nextPubk  = BIP32TestVectors[2]['seedCompPubKey']
      nextChain = BIP32TestVectors[2]['seedCC']

      chA160    = hash160(nextPubk.toBinStr())
      chScript  = hash160_to_p2pkhash_script(chA160)
      chScrAddr = SCRADDR_P2PKH_BYTE + chA160


      abek = ABEK_Generic()
      abek.isWatchOnly = True
      abek.sbdPrivKeyData = NULLSBD()
      abek.sbdPublicKey33 = sbdPubk.copy()
      abek.sbdChaincode   = sbdChain.copy()
      abek.useCompressPub = True

      self.assertRaises(KeyDataError, abek.spawnChild, nextIdx, privSpawnReqd=True)

      childAbek = abek.spawnChild(nextIdx, fsync=False)

      self.assertEqual(childAbek.sbdPrivKeyData, NULLSBD())
      self.assertEqual(childAbek.sbdPublicKey33, nextPubk)
      self.assertEqual(childAbek.sbdChaincode,   nextChain)
      self.assertEqual(childAbek.useCompressPub, True)
      self.assertEqual(childAbek.isUsed, False)
      self.assertEqual(childAbek.privKeyNextUnlock, False)
      self.assertEqual(childAbek.akpParScrAddr, None)
      self.assertEqual(childAbek.childIndex, nextIdx)
      self.assertEqual(childAbek.childPoolSize, 5)
      self.assertEqual(childAbek.maxChildren, UINT32_MAX)
      self.assertEqual(childAbek.rawScript, chScript)
      self.assertEqual(childAbek.scrAddrStr, chScrAddr)
      #self.assertEqual(childAbek.akpChildByIndex, {})
      #self.assertEqual(childAbek.akpChildByScrAddr, {})
      self.assertEqual(childAbek.lowestUnusedChild, 0)
      self.assertEqual(childAbek.nextChildToCalc,   0)
      self.assertEqual(childAbek.akpParentRef, None)
      self.assertEqual(childAbek.masterEkeyRef, None)


      # Test setting the child ref, which is normally done for you if fsync=True
      abek.addChildRef(childAbek)
      self.assertEqual(childAbek.akpParScrAddr, parScrAddr)


      



   #############################################################################
   def testInitABEK(self):
      #leaf = makeABEKGenericClass()
      abek = ABEK_Generic()

      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']

      a160    = hash160(sbdPubk.toBinStr())
      rawScr  = hash160_to_p2pkhash_script(a160)
      scrAddr = SCRADDR_P2PKH_BYTE + a160

      t = long(RightNow())
      abek.initializeAKP(isWatchOnly=False,
                         privCryptInfo=NULLCRYPTINFO(),
                         sbdPrivKeyData=sbdPriv,
                         sbdPublicKey33=sbdPubk,
                         sbdChaincode=sbdChain,
                         privKeyNextUnlock=False,
                         akpParScrAddr=None,
                         childIndex=None,
                         useCompressPub=True,
                         isUsed=True,
                         keyBornTime=t,
                         keyBornBlock=t)

      # Recompute unique ID directly for comparison
      childAbek  = abek.spawnChild(0x7fffffff, fsync=False, forIDCompute=True)
      child256  = hash256(childAbek.getScrAddr())
      firstByte = binary_to_int(child256[0])
      newFirst  = firstByte ^ binary_to_int(ADDRBYTE)
      uidBin = int_to_binary(newFirst) + child256[1:6]
      uidB58 = binary_to_base58(uidBin)

                           
      self.assertEqual(abek.isWatchOnly, False)
      self.assertEqual(abek.sbdPrivKeyData, sbdPriv)
      self.assertEqual(abek.getPlainPrivKeyCopy(), sbdPriv)
      self.assertEqual(abek.sbdPublicKey33, sbdPubk)
      self.assertEqual(abek.sbdChaincode, sbdChain)
      self.assertEqual(abek.useCompressPub, True)
      self.assertEqual(abek.isUsed, True)
      self.assertEqual(abek.keyBornTime, t)
      self.assertEqual(abek.keyBornBlock, t)
      self.assertEqual(abek.privKeyNextUnlock, False)
      self.assertEqual(abek.akpParScrAddr, None)
      self.assertEqual(abek.childIndex, None)
      self.assertEqual(abek.childPoolSize, 5)
      self.assertEqual(abek.maxChildren, UINT32_MAX)
      self.assertEqual(abek.rawScript, rawScr)
      self.assertEqual(abek.scrAddrStr, scrAddr)
      self.assertEqual(abek.uniqueIDBin, uidBin)
      self.assertEqual(abek.uniqueIDB58, uidB58)
      self.assertEqual(abek.akpChildByIndex, {})
      self.assertEqual(abek.akpChildByScrAddr, {})
      self.assertEqual(abek.lowestUnusedChild, 0)
      self.assertEqual(abek.nextChildToCalc,   0)
      self.assertEqual(abek.akpParentRef, None)
      self.assertEqual(abek.masterEkeyRef, None)

      self.assertEqual(abek.TREELEAF, False)
      self.assertEqual(abek.getName(), 'ABEK_Generic')
      self.assertEqual(abek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Available)

      self.assertEqual(abek.getPlainPrivKeyCopy(), sbdPriv)

   #############################################################################
   def testKeyPool_D1(self):
      """
      Doesn't test the accuracy of ABEK calculations, only the keypool sizes
      """
      mockwlt = MockWalletFile()
      echain = ABEK_StdChainExt()
      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']


      # Do this both for priv-key-based derivation and WO-based deriv
      for testWatchOnly in [True,False]:
         echain.initializeAKP(isWatchOnly=testWatchOnly,
                              privCryptInfo=NULLCRYPTINFO(),
                              sbdPrivKeyData=sbdPriv,
                              sbdPublicKey33=sbdPubk,
                              sbdChaincode=sbdChain,
                              privKeyNextUnlock=False,
                              akpParScrAddr=None,
                              childIndex=None,
                              useCompressPub=True,
                              isUsed=True)

         # Test privKeyAvail methods
         if testWatchOnly:
            self.assertEqual(echain.getPrivKeyAvailability(), PRIV_KEY_AVAIL.WatchOnly)
         else:
            self.assertEqual(echain.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Available)
      
         echain.wltFileRef = mockwlt
         echain.setChildPoolSize(5)

      
         self.assertEqual(echain.isWatchOnly,    testWatchOnly)
         self.assertEqual(echain.sbdPublicKey33, sbdPubk)
         self.assertEqual(echain.sbdChaincode,   sbdChain)

         if not testWatchOnly:
            self.assertEqual(echain.sbdPrivKeyData, sbdPriv)
            self.assertEqual(echain.getPlainPrivKeyCopy(), sbdPriv)

         self.assertEqual(echain.lowestUnusedChild,   0)
         self.assertEqual(echain.nextChildToCalc,     0)
         self.assertEqual(echain.childPoolSize,       5)

         echain.fillKeyPoolRecurse()

         self.assertEqual(echain.lowestUnusedChild,  0)
         self.assertEqual(echain.nextChildToCalc,    5)
         self.assertEqual(echain.childPoolSize,      5)



   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testKeyPool_D2(self):
      """
      Doesn't test the accuracy of ABEK calculations, only the keypool sizes
      """
      mockwlt  = MockWalletFile()
      awlt   = ABEK_StdWallet()

      self.assertRaises(ChildDeriveError, awlt.getChildClass, 2)
      self.assertRaises(ChildDeriveError, awlt.getChildClass, HARDBIT)
      self.assertRaises(ChildDeriveError, awlt.getChildClass, 2+HARDBIT)

      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']

      for testWatchOnly in [True,False]:
         awlt.initializeAKP(  isWatchOnly=testWatchOnly,
                              privCryptInfo=NULLCRYPTINFO(),
                              sbdPrivKeyData=sbdPriv,
                              sbdPublicKey33=sbdPubk,
                              sbdChaincode=sbdChain,
                              privKeyNextUnlock=False,
                              akpParScrAddr=None,
                              childIndex=None,
                              useCompressPub=True,
                              isUsed=True)
      
   
         awlt.wltFileRef = mockwlt
      
         self.assertEqual(awlt.isWatchOnly,    testWatchOnly)
         self.assertEqual(awlt.sbdPublicKey33, sbdPubk)
         self.assertEqual(awlt.sbdChaincode,   sbdChain)

         if not testWatchOnly:
            self.assertEqual(awlt.sbdPrivKeyData, sbdPriv)
            self.assertEqual(awlt.getPlainPrivKeyCopy(), sbdPriv)

         self.assertEqual(awlt.lowestUnusedChild, 0)
         self.assertEqual(awlt.nextChildToCalc,   0)

         awlt.fillKeyPoolRecurse()

         self.assertEqual(awlt.lowestUnusedChild,  0)
         self.assertEqual(awlt.nextChildToCalc,    2)
         self.assertEqual(len(awlt.akpChildByIndex), 2)
         self.assertEqual(awlt.akpChildByIndex[0].__class__, ABEK_StdChainExt)
         self.assertEqual(awlt.akpChildByIndex[1].__class__, ABEK_StdChainInt)
         self.assertEqual(awlt.akpChildByIndex[0].childPoolSize, 
                                       DEFAULT_CHILDPOOLSIZE['ABEK_StdChainExt'])
         self.assertEqual(awlt.akpChildByIndex[1].childPoolSize, 
                                       DEFAULT_CHILDPOOLSIZE['ABEK_StdChainInt'])







   #############################################################################
   def testABEK_seedCalc(self):
      mockwlt  = MockWalletFile()
      abekSeed = ABEK_StdBip32Seed()
      abekSeed.wltFileRef = mockwlt

      WRONGPUBK = SecureBinaryData().GenerateRandom(33)
   
      abekSeed.privCryptInfo = NULLCRYPTINFO()
      abekSeed.initializeFromSeed(SEEDTEST[0]['Seed'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[0]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[0]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[0]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[0]['Seed'])
      
      abekSeed.initializeFromSeed(SEEDTEST[0]['Seed'], 
                        verifyPub=SEEDTEST[0]['Pubk'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[0]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[0]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[0]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[0]['Seed'])

      self.assertRaises(KeyDataError, abekSeed.initializeFromSeed, 
                        SEEDTEST[0]['Seed'], verifyPub=WRONGPUBK)



      abekSeed.initializeFromSeed(SEEDTEST[1]['Seed'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[1]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[1]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[1]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[1]['Seed'])
      
      abekSeed.initializeFromSeed(SEEDTEST[1]['Seed'], 
                        verifyPub=SEEDTEST[1]['Pubk'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[1]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[1]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[1]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[1]['Seed'])

      self.assertRaises(KeyDataError, abekSeed.initializeFromSeed, 
                        SEEDTEST[1]['Seed'], verifyPub=WRONGPUBK)


   #############################################################################
   def testABEK_newSeed(self):
      mockwlt  = MockWalletFile()
      abekSeed = ABEK_StdBip32Seed()
      abekSeed.wltFileRef = mockwlt
   
      abekSeed.privCryptInfo = NULLCRYPTINFO()

      # Should fail for seed being too small
      self.assertRaises(KeyDataError, abekSeed.createNewSeed, 8, None)

      # Should fail for not supplying extra entropy
      self.assertRaises(KeyDataError, abekSeed.createNewSeed, 16, None)

      # Extra entropy should be pulled from external sources!  Such as
      # system files, screenshots, uninitialized RAM states... only do
      # it the following way for testing!
      entropy = SecureBinaryData().GenerateRandom(8)

      for seedsz in [16, 20, 256]:
         abekSeed.createNewSeed(seedsz, entropy, fillPool=False)


   #############################################################################
   def testGetParentList(self):
      mockwlt  = MockWalletFile()
      abekSeed = ABEK_StdBip32Seed()
      abekSeed.wltFileRef = mockwlt
      abekSeed.privCryptInfo = NULLCRYPTINFO()
      entropy = SecureBinaryData().GenerateRandom(8)
      abekSeed.createNewSeed(16, entropy, fillPool=False)

      # Test root itself, shoudl be empty
      self.assertEqual(abekSeed.getParentList(), [])

      abekSeed.fillKeyPoolRecurse()

      # Test first-level parent lists
      for widx,abekWlt in abekSeed.akpChildByIndex.iteritems():
         expect = [[abekSeed, widx]]
         self.assertEqual(abekWlt.getParentList(), expect)

      # Test two-levels:
      for widx,abekWlt in abekSeed.akpChildByIndex.iteritems():
         for cidx,abekChn in abekWlt.akpChildByIndex.iteritems():
            expect = [[abekSeed, widx], [abekWlt, cidx]]
            self.assertEqual(abekChn.getParentList(), expect)

      # Test two-levels:
      for widx,abekWlt in abekSeed.akpChildByIndex.iteritems():
         for cidx,abekChn in abekWlt.akpChildByIndex.iteritems():
            expect = [[abekSeed, widx], [abekWlt, cidx]]
            self.assertEqual(abekChn.getParentList(), expect)

      # Test three-levels:
      for widx,abekWlt in abekSeed.akpChildByIndex.iteritems():
         for cidx,abekChn in abekWlt.akpChildByIndex.iteritems():
            for lidx,abekLeaf in abekChn.akpChildByIndex.iteritems():
               expect = [[abekSeed, widx], [abekWlt, cidx], [abekChn, lidx]]
               self.assertEqual(abekLeaf.getParentList(), expect)

      # Test up to different base
      for widx,abekWlt in abekSeed.akpChildByIndex.iteritems():
         for cidx,abekChn in abekWlt.akpChildByIndex.iteritems():
            for lidx,abekLeaf in abekChn.akpChildByIndex.iteritems():
               expect = [[abekWlt, cidx], [abekChn, lidx]]
               wsa = abekWlt.getScrAddr()
               self.assertEqual(abekLeaf.getParentList(wsa), expect)
               self.assertRaises(ChildDeriveError, abekLeaf.getParentList, 'abc')
   
   #############################################################################
   # Haven't written these yet
   @unittest.skipIf(skipFlagExists(), '')
   def testABEK_serialize(self):
      pass
      
   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testABEK_serRoundTrip(self):
      pass
         
   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testABEK_serRoundTripWalletEntry(self):
      pass


################################################################################
################################################################################
#
# Armory BIP32 Extended Key tests (WITH ENCRYPTION)
#
################################################################################
################################################################################

################################################################################
class ABEK_Encrypted_Tests(unittest.TestCase):

   #############################################################################
   def setUp(self):
      self.mockwlt  = MockWalletFile()

      self.password = SecureBinaryData('hello')
      master32 = SecureBinaryData('\x3e'*32)
      randomiv = SecureBinaryData('\x7d'*8)

      # Create a KDF to be used for encryption key password
      self.kdf = KdfObject('ROMIXOV2', memReqd=32*KILOBYTE,
                                       numIter=1, 
                                       salt=SecureBinaryData('\x21'*32))

      # Create the new master encryption key to be used to encrypt priv keys
      self.ekey = EncryptionKey().createNewMasterKey(self.kdf, 'AE256CBC', 
                     self.password, preGenKey=master32, preGenIV8=randomiv)

      # This will be attached to each ABEK object, to define its encryption
      self.privACI = ArmoryCryptInfo(NULLKDF, 'AE256CBC', 
                                 self.ekey.ekeyID, 'PUBKEY20')

      
   #############################################################################
   def tearDown(self):
      pass
      
   #############################################################################
   def testSpawnABEK(self):
      #leaf = makeABEKGenericClass()
      abek = ABEK_Generic()
      
      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']

      a160    = hash160(sbdPubk.toBinStr())
      rawScr  = hash160_to_p2pkhash_script(a160)
      scrAddr = SCRADDR_P2PKH_BYTE + a160

      # First some prep for encryption/decryption, and verify outputs
      self.ekey.unlock(self.password)
      iv = SecureBinaryData(hash256(sbdPubk.toBinStr())[:16])
      privCrypt = self.privACI.encrypt(sbdPriv,   ekeyObj=self.ekey, ivData=iv)
      decrypted = self.privACI.decrypt(privCrypt, ekeyObj=self.ekey, ivData=iv)
      self.assertEqual(sbdPriv, decrypted)
      self.ekey.lock()


      t = long(RightNow())
      abek.initializeAKP(isWatchOnly=False,
                         privCryptInfo=self.privACI,
                         sbdPrivKeyData=privCrypt,
                         sbdPublicKey33=sbdPubk,
                         sbdChaincode=sbdChain,
                         privKeyNextUnlock=False,
                         akpParScrAddr=None,
                         childIndex=None,
                         useCompressPub=True,
                         isUsed=True,
                         keyBornTime=t,
                         keyBornBlock=t)

      abek.masterEkeyRef = self.ekey


      # Need to test the privkey available func
      self.ekey.lock()
      self.assertEqual(abek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.NeedDecrypt)
      self.ekey.unlock(self.password)
      self.assertEqual(abek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Available)
      self.ekey.lock()
      self.assertEqual(abek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.NeedDecrypt)


      # Recompute unique ID directly for comparison
      childAbek  = abek.spawnChild(0x7fffffff, fsync=False, forIDCompute=True)
      child256  = hash256(childAbek.getScrAddr())
      firstByte = binary_to_int(child256[0])
      newFirst  = firstByte ^ binary_to_int(ADDRBYTE)
      uidBin = int_to_binary(newFirst) + child256[1:6]
      uidB58 = binary_to_base58(uidBin)

      self.ekey.lock()
      self.assertRaises(WalletLockError, abek.getPlainPrivKeyCopy)
      self.ekey.unlock(self.password)
      self.assertEqual(abek.sbdPrivKeyData, privCrypt)
      self.assertEqual(abek.getPlainPrivKeyCopy(), sbdPriv)
      self.ekey.lock()

      self.assertEqual(abek.isWatchOnly, False)
      self.assertEqual(abek.sbdPublicKey33, sbdPubk)
      self.assertEqual(abek.sbdChaincode, sbdChain)
      self.assertEqual(abek.useCompressPub, True)
      self.assertEqual(abek.isUsed, True)
      self.assertEqual(abek.keyBornTime, t)
      self.assertEqual(abek.keyBornBlock, t)
      self.assertEqual(abek.privKeyNextUnlock, False)
      self.assertEqual(abek.akpParScrAddr, None)
      self.assertEqual(abek.childIndex, None)
      self.assertEqual(abek.childPoolSize, 5)
      self.assertEqual(abek.maxChildren, UINT32_MAX)
      self.assertEqual(abek.rawScript, rawScr)
      self.assertEqual(abek.scrAddrStr, scrAddr)
      self.assertEqual(abek.uniqueIDBin, uidBin)
      self.assertEqual(abek.uniqueIDB58, uidB58)
      self.assertEqual(abek.akpChildByIndex, {})
      self.assertEqual(abek.akpChildByScrAddr, {})
      self.assertEqual(abek.lowestUnusedChild, 0)
      self.assertEqual(abek.nextChildToCalc,   0)
      self.assertEqual(abek.akpParentRef, None)
      self.assertEqual(abek.privCryptInfo.serialize(), self.privACI.serialize())

      self.assertEqual(abek.TREELEAF, False)
      self.assertEqual(abek.getName(), 'ABEK_Generic')



   #############################################################################
   def testSpawnABEK(self):
      # Start with this key pair
      sbdPriv  = SecureBinaryData(BIP32TestVectors[1]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[1]['seedCompPubKey']
      sbdChain = BIP32TestVectors[1]['seedCC']
      nextIdx  = BIP32TestVectors[1]['nextChild']
      parA160    = hash160(sbdPubk.toBinStr())
      parScript  = hash160_to_p2pkhash_script(parA160)
      parScrAddr = SCRADDR_P2PKH_BYTE + parA160

      # Derive this keypair
      nextPriv  = SecureBinaryData(BIP32TestVectors[2]['seedKey'].toBinStr()[1:])
      nextPubk  = BIP32TestVectors[2]['seedCompPubKey']
      nextChain = BIP32TestVectors[2]['seedCC']
      chA160    = hash160(nextPubk.toBinStr())
      chScript  = hash160_to_p2pkhash_script(chA160)
      chScrAddr = SCRADDR_P2PKH_BYTE + chA160


      # First some prep for encryption/decryption, and verify RT encrypt/decrypt
      self.ekey.unlock(self.password)
      iv1 = SecureBinaryData(hash256(sbdPubk.toBinStr())[:16])
      iv2 = SecureBinaryData(hash256(nextPubk.toBinStr())[:16])

      privCrypt1 = self.privACI.encrypt(sbdPriv,    ekeyObj=self.ekey, ivData=iv1)
      privCrypt2 = self.privACI.encrypt(nextPriv,   ekeyObj=self.ekey, ivData=iv2)

      decrypted1 = self.privACI.decrypt(privCrypt1, ekeyObj=self.ekey, ivData=iv1)
      decrypted2 = self.privACI.decrypt(privCrypt2, ekeyObj=self.ekey, ivData=iv2)

      self.assertEqual(sbdPriv, decrypted1)
      self.assertEqual(nextPriv, decrypted2)
      self.ekey.lock()



      abek = ABEK_Generic()
      abek.isWatchOnly = False
      abek.privCryptInfo  = self.privACI
      abek.sbdPrivKeyData = privCrypt1
      abek.sbdPublicKey33 = sbdPubk.copy()
      abek.sbdChaincode   = sbdChain.copy()
      abek.useCompressPub = True
      abek.masterEkeyRef = self.ekey
      abek.privKeyNextUnlock = False
      abek.wltFileRef = self.mockwlt

      self.ekey.unlock(self.password)
      childAbek = abek.spawnChild(nextIdx, fsync=False, privSpawnReqd=True)

      self.assertEqual(childAbek.sbdPrivKeyData, privCrypt2)
      self.assertEqual(childAbek.getPlainPrivKeyCopy(), nextPriv)

      self.assertEqual(childAbek.sbdPublicKey33, nextPubk)
      self.assertEqual(childAbek.sbdChaincode,   nextChain)
      self.assertEqual(childAbek.useCompressPub, True)
      self.assertEqual(childAbek.isUsed, False)
      self.assertEqual(childAbek.privKeyNextUnlock, False)
      self.assertEqual(childAbek.akpParScrAddr, None)
      self.assertEqual(childAbek.childIndex, nextIdx)
      self.assertEqual(childAbek.childPoolSize, 5)
      self.assertEqual(childAbek.maxChildren, UINT32_MAX)
      self.assertEqual(childAbek.rawScript, chScript)
      self.assertEqual(childAbek.scrAddrStr, chScrAddr)
      self.assertEqual(childAbek.lowestUnusedChild, 0)
      self.assertEqual(childAbek.nextChildToCalc,   0)
      self.assertEqual(childAbek.akpParentRef, None)
      
      # Check the uniqueID, by spawning another child
      subCh = childAbek.spawnChild(0x7fffffff, fsync=False, forIDCompute=True)
      ch256  = hash256(subCh.getScrAddr())
      firstByte = binary_to_int(ch256[0])
      newFirst  = firstByte ^ binary_to_int(ADDRBYTE)
      uidBin = int_to_binary(newFirst) + ch256[1:6]
      uidB58 = binary_to_base58(uidBin)
      self.assertEqual(childAbek.uniqueIDBin, uidBin)
      self.assertEqual(childAbek.uniqueIDB58, uidB58)

      self.ekey.lock()
      self.assertRaises(WalletLockError, abek.spawnChild, nextIdx, privSpawnReqd=True)

   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testSpawn_CreateNextUnlock(self):
      # Start with this key pair
      sbdPriv  = SecureBinaryData(BIP32TestVectors[1]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[1]['seedCompPubKey']
      sbdChain = BIP32TestVectors[1]['seedCC']
      nextIdx  = BIP32TestVectors[1]['nextChild']
      parA160    = hash160(sbdPubk.toBinStr())
      parScript  = hash160_to_p2pkhash_script(parA160)
      parScrAddr = SCRADDR_P2PKH_BYTE + parA160

      # Derive this keypair
      nextPriv  = SecureBinaryData(BIP32TestVectors[2]['seedKey'].toBinStr()[1:])
      nextPubk  = BIP32TestVectors[2]['seedCompPubKey']
      nextChain = BIP32TestVectors[2]['seedCC']
      chA160    = hash160(nextPubk.toBinStr())
      chScript  = hash160_to_p2pkhash_script(chA160)
      chScrAddr = SCRADDR_P2PKH_BYTE + chA160

      # First some prep for encryption/decryption, and verify RT encrypt/decrypt
      self.ekey.unlock(self.password)
      iv1 = SecureBinaryData(hash256(sbdPubk.toBinStr())[:16])
      iv2 = SecureBinaryData(hash256(nextPubk.toBinStr())[:16])

      privCrypt1 = self.privACI.encrypt(sbdPriv,    ekeyObj=self.ekey, ivData=iv1)
      privCrypt2 = self.privACI.encrypt(nextPriv,   ekeyObj=self.ekey, ivData=iv2)

      decrypted1 = self.privACI.decrypt(privCrypt1, ekeyObj=self.ekey, ivData=iv1)
      decrypted2 = self.privACI.decrypt(privCrypt2, ekeyObj=self.ekey, ivData=iv2)

      self.assertEqual(sbdPriv, decrypted1)
      self.assertEqual(nextPriv, decrypted2)
      self.ekey.lock()

      abek = ABEK_Generic()
      abek.isWatchOnly = False
      abek.privCryptInfo  = self.privACI
      abek.sbdPrivKeyData = privCrypt1
      abek.sbdPublicKey33 = sbdPubk.copy()
      abek.sbdChaincode   = sbdChain.copy()
      abek.useCompressPub = True
      abek.masterEkeyRef = self.ekey
      abek.privKeyNextUnlock = False
      abek.wltFileRef = self.mockwlt

      # Now DON'T unlock before spawning
      #self.ekey.unlock(self.password)
      self.ekey.lock()
      childAbek = abek.spawnChild(nextIdx, fsync=False)

      self.assertEqual(childAbek.sbdPublicKey33, nextPubk)
      self.assertEqual(childAbek.sbdChaincode,   nextChain)
      self.assertEqual(childAbek.useCompressPub, True)
      self.assertEqual(childAbek.isUsed, False)

      self.assertEqual(childAbek.getPrivKeyAvailability(), PRIV_KEY_AVAIL.NextUnlock)
      self.assertEqual(childAbek.privKeyNextUnlock, True)

      self.assertEqual(childAbek.akpParScrAddr, None)
      self.assertEqual(childAbek.childIndex, nextIdx)
      self.assertEqual(childAbek.childPoolSize, 5)
      self.assertEqual(childAbek.maxChildren, UINT32_MAX)
      self.assertEqual(childAbek.rawScript, chScript)
      self.assertEqual(childAbek.scrAddrStr, chScrAddr)
      



   #############################################################################
   def testKeyPool_D1(self):
      """
      Doesn't test the accuracy of ABEK calculations, only the keypool sizes
      """
      echain = ABEK_StdChainExt()
      mockwlt = MockWalletFile()
      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']

      a160    = hash160(sbdPubk.toBinStr())
      rawScr  = hash160_to_p2pkhash_script(a160)
      scrAddr = SCRADDR_P2PKH_BYTE + a160

      # First some prep for encryption/decryption, and verify outputs
      self.ekey.unlock(self.password)
      iv = SecureBinaryData(hash256(sbdPubk.toBinStr())[:16])
      privCrypt = self.privACI.encrypt(sbdPriv,   ekeyObj=self.ekey, ivData=iv)
      decrypted = self.privACI.decrypt(privCrypt, ekeyObj=self.ekey, ivData=iv)
      self.assertEqual(sbdPriv, decrypted)
      self.ekey.lock()


      t = long(RightNow())
      echain.initializeAKP(isWatchOnly=False,
                           privCryptInfo=self.privACI,
                           sbdPrivKeyData=privCrypt,
                           sbdPublicKey33=sbdPubk,
                           sbdChaincode=sbdChain,
                           privKeyNextUnlock=False,
                           akpParScrAddr=None,
                           childIndex=None,
                           useCompressPub=True,
                           isUsed=True,
                           keyBornTime=t,
                           keyBornBlock=t)

      echain.masterEkeyRef = self.ekey
      echain.wltFileRef = mockwlt
      echain.setChildPoolSize(5)

      
      self.assertEqual(echain.isWatchOnly,    False)
      self.assertEqual(echain.sbdPublicKey33, sbdPubk)
      self.assertEqual(echain.sbdChaincode,   sbdChain)

      #self.assertEqual(echain.sbdPrivKeyData, sbdPriv)
      self.assertRaises(WalletLockError, echain.getPlainPrivKeyCopy)

      self.assertEqual(echain.lowestUnusedChild,   0)
      self.assertEqual(echain.nextChildToCalc,     0)
      self.assertEqual(echain.childPoolSize,       5)

      self.ekey.unlock(self.password)
      echain.fillKeyPoolRecurse()

      self.assertEqual(echain.lowestUnusedChild,  0)
      self.assertEqual(echain.nextChildToCalc,    5)
      self.assertEqual(echain.childPoolSize,      5)

      # Check doing some sanity checking on the children, not accuracy check
      for i,ch in echain.akpChildByIndex.iteritems():
         priv = ch.getPlainPrivKeyCopy()
         pub = CryptoECDSA().ComputePublicKey(priv)
         pub = CryptoECDSA().CompressPoint(pub)
         self.assertEqual(pub, ch.sbdPublicKey33)
         self.assertEqual(ch.masterEkeyRef, self.ekey)
         self.assertTrue(ch.privCryptInfo.useEncryption())
         self.assertEqual(ch.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Available)

      


   #############################################################################
   @unittest.skipIf(skipFlagExists(), '')
   def testKeyPool_D2(self):
      """
      Doesn't test the accuracy of ABEK calculations, only the keypool sizes
      """
      mockwlt  = MockWalletFile()
      awlt   = ABEK_StdWallet()

      sbdPriv  = SecureBinaryData(BIP32TestVectors[0]['seedKey'].toBinStr()[1:])
      sbdPubk  = BIP32TestVectors[0]['seedCompPubKey']
      sbdChain = BIP32TestVectors[0]['seedCC']

      # First some prep for encryption/decryption, and verify outputs
      self.ekey.unlock(self.password)
      iv = SecureBinaryData(hash256(sbdPubk.toBinStr())[:16])
      privCrypt = self.privACI.encrypt(sbdPriv,   ekeyObj=self.ekey, ivData=iv)
      decrypted = self.privACI.decrypt(privCrypt, ekeyObj=self.ekey, ivData=iv)
      self.assertEqual(sbdPriv, decrypted)
      self.ekey.lock()

      t = long(RightNow())
      awlt.initializeAKP(isWatchOnly=False,
                           privCryptInfo=self.privACI,
                           sbdPrivKeyData=privCrypt,
                           sbdPublicKey33=sbdPubk,
                           sbdChaincode=sbdChain,
                           privKeyNextUnlock=False,
                           akpParScrAddr=None,
                           childIndex=None,
                           useCompressPub=True,
                           isUsed=True,
                           keyBornTime=t,
                           keyBornBlock=t)

      awlt.masterEkeyRef = self.ekey
      awlt.wltFileRef = mockwlt
      awlt.setChildPoolSize(5)

      
      self.assertEqual(awlt.isWatchOnly,    False)
      self.assertEqual(awlt.sbdPublicKey33, sbdPubk)
      self.assertEqual(awlt.sbdChaincode,   sbdChain)

      #self.assertEqual(awlt.sbdPrivKeyData, sbdPriv)
      #self.assertEqual(awlt.getPlainPrivKeyCopy(), sbdPriv)

      self.assertEqual(awlt.lowestUnusedChild, 0)
      self.assertEqual(awlt.nextChildToCalc,   0)

      self.ekey.unlock(self.password)
      awlt.fillKeyPoolRecurse()

      self.assertEqual(awlt.lowestUnusedChild,  0)
      self.assertEqual(awlt.nextChildToCalc,    2)
      self.assertEqual(len(awlt.akpChildByIndex), 2)
      self.assertEqual(awlt.akpChildByIndex[0].__class__, ABEK_StdChainExt)
      self.assertEqual(awlt.akpChildByIndex[1].__class__, ABEK_StdChainInt)
      self.assertEqual(awlt.akpChildByIndex[0].childPoolSize, 
                                    DEFAULT_CHILDPOOLSIZE['ABEK_StdChainExt'])
      self.assertEqual(awlt.akpChildByIndex[1].childPoolSize, 
                                    DEFAULT_CHILDPOOLSIZE['ABEK_StdChainInt'])

      # Check doing some sanity checking on the children, not accuracy check
      for i,ch in awlt.akpChildByIndex.iteritems():
         for j,ch2 in ch.akpChildByIndex.iteritems():
            priv = ch.getPlainPrivKeyCopy()
            pub = CryptoECDSA().ComputePublicKey(priv)
            pub = CryptoECDSA().CompressPoint(pub)
            self.assertEqual(pub, ch.sbdPublicKey33)
            self.assertEqual(ch.masterEkeyRef, self.ekey)
            self.assertTrue(ch.privCryptInfo.useEncryption())
            self.assertEqual(ch.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Available)



   #############################################################################
   def testABEK_seedCalc(self):
      mockwlt  = MockWalletFile()
      abekSeed = ABEK_StdBip32Seed()
      abekSeed.wltFileRef = mockwlt
      abekSeed.masterEkeyRef = self.ekey

      WRONGPUBK = SecureBinaryData().GenerateRandom(33)

      self.ekey.lock()
      self.assertRaises(WalletLockError, abekSeed.initializeFromSeed, \
                                       SEEDTEST[0]['Seed'], fillPool=False)
      self.ekey.unlock(self.password)
   
      abekSeed.privCryptInfo = self.privACI
      abekSeed.initializeFromSeed(SEEDTEST[0]['Seed'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[0]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[0]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[0]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[0]['Seed'])
      self.assertFalse(abekSeed.sbdPrivKeyData == SEEDTEST[0]['Priv'])
      self.assertFalse(abekSeed.sbdSeedData    == SEEDTEST[0]['Seed'])
      self.assertEqual(abekSeed.seedCryptInfo.keySource, self.ekey.ekeyID)
      
      abekSeed.initializeFromSeed(SEEDTEST[0]['Seed'], 
                        verifyPub=SEEDTEST[0]['Pubk'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[0]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[0]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[0]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[0]['Seed'])
      self.assertFalse(abekSeed.sbdPrivKeyData == SEEDTEST[0]['Priv'])
      self.assertFalse(abekSeed.sbdSeedData    == SEEDTEST[0]['Seed'])
      self.assertEqual(abekSeed.seedCryptInfo.keySource, self.ekey.ekeyID)

      self.assertRaises(KeyDataError, abekSeed.initializeFromSeed, 
                        SEEDTEST[0]['Seed'], verifyPub=WRONGPUBK)



      abekSeed.initializeFromSeed(SEEDTEST[1]['Seed'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[1]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[1]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[1]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[1]['Seed'])
      self.assertFalse(abekSeed.sbdPrivKeyData == SEEDTEST[0]['Priv'])
      self.assertFalse(abekSeed.sbdSeedData    == SEEDTEST[0]['Seed'])
      self.assertEqual(abekSeed.seedCryptInfo.keySource, self.ekey.ekeyID)
      
      abekSeed.initializeFromSeed(SEEDTEST[1]['Seed'], 
                        verifyPub=SEEDTEST[1]['Pubk'], fillPool=False)
      self.assertEqual(abekSeed.getPlainPrivKeyCopy(), SEEDTEST[1]['Priv'])
      self.assertEqual(abekSeed.sbdPublicKey33,        SEEDTEST[1]['Pubk'])
      self.assertEqual(abekSeed.sbdChaincode,          SEEDTEST[1]['Chain'])
      self.assertEqual(abekSeed.getPlainSeedCopy(),    SEEDTEST[1]['Seed'])
      self.assertFalse(abekSeed.sbdPrivKeyData == SEEDTEST[0]['Priv'])
      self.assertFalse(abekSeed.sbdSeedData    == SEEDTEST[0]['Seed'])
      self.assertEqual(abekSeed.seedCryptInfo.keySource, self.ekey.ekeyID)

      self.assertRaises(KeyDataError, abekSeed.initializeFromSeed, 
                        SEEDTEST[1]['Seed'], verifyPub=WRONGPUBK)


   #############################################################################
   def testABEK_newSeed(self):
      mockwlt  = MockWalletFile()
      abekSeed = ABEK_StdBip32Seed()
      abekSeed.wltFileRef = mockwlt
      abekSeed.masterEkeyRef = self.ekey
   
      abekSeed.privCryptInfo = self.privACI

      self.ekey.unlock(self.password)
      # Should fail for seed being too small
      self.assertRaises(KeyDataError, abekSeed.createNewSeed, 8, None)

      # Should fail for not supplying extra entropy
      self.assertRaises(KeyDataError, abekSeed.createNewSeed, 16, None)

      # Extra entropy should be pulled from external sources!  Such as
      # system files, screenshots, uninitialized RAM states... only do
      # it the following way for testing!
      entropy = SecureBinaryData().GenerateRandom(8)

      self.ekey.lock()
      for seedsz in [16, 20, 256]:
         self.assertRaises(WalletLockError, abekSeed.createNewSeed, seedsz, entropy, fillPool=False)

      self.ekey.unlock(self.password)
      for seedsz in [16, 20, 256]:
         abekSeed.createNewSeed(seedsz, entropy, fillPool=False)




################################################################################
################################################################################
#
# Armory 135 TESTS  (NO ENCRYPTION)
#
################################################################################
################################################################################

class A135_NoCrypt_Tests(unittest.TestCase):

   #############################################################################
   def setUp(self):
      pass

      self.rootID    = 'zrPzapKR'
      self.rootLine1 = 'okkn weod aajf skrs jdrj rafa gjtr saho eari'.replace(' ','')
      self.rootLine2 = 'rdeg jaah soea ugas jeot niua jdeg hkou gsih'.replace(' ','')
      self.binSeed   = readSixteenEasyBytes(self.rootLine1)[0] + \
                       readSixteenEasyBytes(self.rootLine2)[0]
      self.chaincode = DeriveChaincodeFromRootKey_135(SecureBinaryData(self.binSeed))


      self.keyList = {}

      self.keyList[0] = { \
         'AddrStr': '13QVfpnE7TWAnkGGpHak1Z9cJVQWTZrYqb',
         'PrivB58': '5JWFgYDRyCqxMcXprSf84RAfPC4p6x2eifXxNwHuqeL137JC11A',
         'PubKeyX': '1a84426c38a0099975d683365436ee3eedaf2c9589c44635aa3808ede5f87081',
         'PubKeyY': '6a905e1f3055c0982307951e5e4150349c5c98a644f3da9aeef9c80f103cf2af' }
      self.keyList[1] = { \
         'AddrStr': '1Dy4cGbv3KKm4EhQYVKvUJQfy6sgmGR4ii',
         'PrivB58': '5KMBzjqDE8dXxtvRaY8dGHnMUNyE6uonDwKgeG44XBsngqTYkf9',
         'PubKeyX': '6c23cc6208a1f6daaa196ba6e763b445555ada6315ebf9465a0b9cb49e813e3a',
         'PubKeyY': '341eb33ed738b6a1ac6a57526a80af2e6841dcf71f287dbe721dd4486d9cf8c4' }
      self.keyList[2] = { \
         'AddrStr': '1BKG36rBdxiYNRQbLCYfPzi6Cf4pW2aRxQ',
         'PrivB58': '5KhpN6mmdiVcKmZtPjqfC41Af7181Dj4JadyU7dDLVefdPcMbZi',
         'PubKeyX': 'eb013f8047ad532a8bcc4d4f69a62887ce82afb574d7fb8a326b9bab82d240fa',
         'PubKeyY': 'a8fdcd604105292cb04c7707da5e42300bc418654f8ffc94e2c83bd5a54e09e2' }
      self.keyList[3] = { \
         'AddrStr': '1NhZfoXMLmohuvAh7Ks67JMx6mpcVq2FCa',
         'PrivB58': '5KaxXWwQgFcp3d5Bqd58xvtBDN8FEPQeRZJDpyxY5LTZ5ALZHE3',
         'PubKeyX': 'd6e6d3031d5d3de48293d97590f5b697089e8e6b40e919a68e2a07c300c1256b',
         'PubKeyY': '3d9b428e0ef9f73bd81c9388e1d8702f477138ca444eed57370d0e31ba9bafe5' }
      self.keyList[4] = { \
         'AddrStr': '1GHvHhrUBL5mMryscJa9uzDnPXeEpqU7Tn',
         'PrivB58': '5Jb4u9bpWDv19y6hu6nAE7cDdQoUrJMoyrwGDjPxMKo8oxULSdn',
         'PubKeyX': 'e40d3923bfffad0cdc6d6a3341c8e669beb1264b86cbfd21229ca8a74cf53ca5',
         'PubKeyY': '587b7a9b18b648cd421d17d45d05e8fc647f7ea02f61b670a2d4c2012e3b717f' }
      self.keyList[5] = { \
         'AddrStr': '1DdAdN2VQXg52YqDssZ4o6XprVgEB4Evpj',
         'PrivB58': '5JxD9BrDhCgWEKfEUG2FBcAk1D667G97hNREg81M5Qzgi9CAgdD',
         'PubKeyX': '7e043899f917288db2962819cd78c8328efb6dd172b9cbe1bfaaf8d745fd3e99',
         'PubKeyY': '746b29150ff3828556595291419d579c824ac2879d83fb3d51d5efea5de4715d' }
      self.keyList[6] = { \
         'AddrStr': '1K9QBzxv2jL7ftMkJ9jghr8dJgZ6u6zhHR',
         'PrivB58': '5K7GHu48sqxnYNhiMNVVoeh8WXnnerrNhL2TWocHngaP8zyUPAr',
         'PubKeyX': 'bbc9cd69dd6977b08d7916c0da81208df0b8a491b0897ca482bd42df47102d6b',
         'PubKeyY': 'f0318b3298ba93831df82b7ce51da5e0e8647a3ecd994f600a84834b424ed2b8' }

      # For reference, here's the first 6 ScrAddrs
      # ROOT: 00ef2ba030696d99d945fea3990e4213c62d042ddd
      # 0: 001a61c02c74328db5122fa9c1d4917f05de86a8c2
      # 1: 008e3bd0ad4a85b3fd3d4998397e8da93635aab664
      # 2: 0071254bf82804253fbafaf49b45fe7f85eba0d3d5
      # 3: 00ee068cf6c7b6fc77326cba37d621aebe834a5257
      # 4: 00a7bd0654e2bebf43acfab6b75a4619e70464cce8
      # 5: 008a78852b767f5b5dc8567dbfa53214e914430789

      for idx,imap in self.keyList.iteritems():
         imap['PrivKey']   = SecureBinaryData(parsePrivateKeyData(imap['PrivB58'])[0])
         imap['PubKey']    = SecureBinaryData(hex_to_binary('04' + imap['PubKeyX'] + imap['PubKeyY']))
         imap['Chaincode'] = self.chaincode.copy()
         imap['ScrAddr']   = SCRADDR_P2PKH_BYTE + hash160(imap['PubKey'].toBinStr())
      
   #############################################################################
   def tearDown(self):
      pass
      

   #############################################################################
   def testInitA135(self):
      #leaf = makeABEKGenericClass()
      a135 = Armory135KeyPair()
         
      self.assertEqual(a135.isWatchOnly, False)
      self.assertEqual(a135.sbdPrivKeyData, NULLSBD())
      self.assertEqual(a135.sbdPublicKey33, NULLSBD())
      self.assertEqual(a135.sbdChaincode, NULLSBD())
      self.assertEqual(a135.useCompressPub, False)
      self.assertEqual(a135.isUsed, False)
      self.assertEqual(a135.keyBornTime, 0)
      self.assertEqual(a135.keyBornBlock, 0)
      self.assertEqual(a135.privKeyNextUnlock, False)
      self.assertEqual(a135.childPoolSize, 1)
      self.assertEqual(a135.maxChildren, 1)
      self.assertEqual(a135.rawScript, None)
      self.assertEqual(a135.scrAddrStr, None)
      self.assertEqual(a135.uniqueIDBin, None)
      self.assertEqual(a135.uniqueIDB58, None)
      self.assertEqual(a135.akpChildByIndex, {})
      self.assertEqual(a135.akpChildByScrAddr, {})
      self.assertEqual(a135.lowestUnusedChild, 0)
      self.assertEqual(a135.nextChildToCalc,   0)
      self.assertEqual(a135.akpParentRef, None)
      self.assertEqual(a135.masterEkeyRef, None)

      self.assertEqual(a135.getName(), 'Armory135KeyPair')
      self.assertEqual(a135.getPrivKeyAvailability(), PRIV_KEY_AVAIL.Uninit)

      self.assertEqual(a135.chainIndex, None)
      self.assertEqual(a135.childIndex, 0)

      # WalletEntry fields
      self.assertEqual(a135.wltFileRef, None)
      self.assertEqual(a135.wltByteLoc, None)
      self.assertEqual(a135.wltEntrySz, None)
      self.assertEqual(a135.isRequired, False)
      self.assertEqual(a135.parEntryID, None)
      self.assertEqual(a135.outerCrypt.serialize(), NULLCRYPTINFO().serialize())
      self.assertEqual(a135.serPayload, None)
      self.assertEqual(a135.defaultPad, 256)
      self.assertEqual(a135.wltParentRef, None)
      self.assertEqual(a135.wltChildRefs, [])
      self.assertEqual(a135.outerEkeyRef, None)
      self.assertEqual(a135.isOpaque,        False)
      self.assertEqual(a135.isUnrecognized,  False)
      self.assertEqual(a135.isUnrecoverable, False)
      self.assertEqual(a135.isDeleted,       False)
      self.assertEqual(a135.isDisabled,      False)
      self.assertEqual(a135.needFsync,       False)

   #############################################################################
   def testInitFromSeed(self):
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = NULLCRYPTINFO()
      a135rt.childPoolSize = 3
      a135rt.initializeFromSeed(seed, fillPool=False)

      self.assertEqual(a135rt.sbdSeedData.toHexStr(), '') # supposed to be empty
      self.assertEqual(a135rt.privCryptInfo.serialize(), NULLCRYPTINFO().serialize())
      self.assertEqual(a135rt.privKeyNextUnlock, False)

      self.assertEqual(a135rt.getPlainSeedCopy().toHexStr(), seed.toHexStr())
      self.assertEqual(a135rt.getUniqueIDB58(), self.rootID)

      self.assertEqual(a135rt.rootLowestUnused, 0)
      self.assertEqual(a135rt.rootNextToCalc,   0)

   #############################################################################
   def testSpawnA135(self):

      for WO in [False, True]:
         a135 = Armory135KeyPair()
         mockwlt = MockWalletFile()

         seed = SecureBinaryData(self.binSeed)
         a135rt = Armory135Root()
         a135rt.privCryptInfo = NULLCRYPTINFO()
         a135rt.childPoolSize = 3
         a135rt.wltFileRef = mockwlt
         a135rt.initializeFromSeed(seed, fillPool=False)

         if WO:
            a135rt.wipePrivateData()


         a135 = a135rt.spawnChild()
         self.assertEqual(a135rt.rootLowestUnused, 0)
         self.assertEqual(a135rt.rootNextToCalc,   1)

         prevScrAddr = a135rt.getScrAddr()
         rootScrAddr = a135rt.getScrAddr()

         kidx = 0
         while kidx+1 in self.keyList:
   
            pub65 = self.keyList[kidx]['PubKey']
            a160  = hash160(pub65.toBinStr())
   
            expectPriv   = self.keyList[kidx]['PrivKey'].copy()
            expectPub    = CryptoECDSA().CompressPoint(pub65)
            expectChain  = self.chaincode.copy()
            expectScript = hash160_to_p2pkhash_script(a160)
            expectScrAddr= script_to_scrAddr(expectScript)
            self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

            if not WO:
               self.assertEqual(a135.sbdPrivKeyData, expectPriv)
               self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)
            else:
               self.assertEqual(a135.sbdPrivKeyData, NULLSBD())
   
            self.assertEqual(a135.isWatchOnly, WO)
            self.assertEqual(a135.sbdPublicKey33, expectPub)
            self.assertEqual(a135.sbdChaincode,   expectChain)
            self.assertEqual(a135.useCompressPub, False)
            self.assertEqual(a135.isUsed, False)
            self.assertEqual(a135.privKeyNextUnlock, False)
            self.assertEqual(a135.akpParScrAddr, prevScrAddr)
            self.assertEqual(a135.childIndex, 0)
            self.assertEqual(a135.childPoolSize, 1)
            self.assertEqual(a135.maxChildren, 1)
            self.assertEqual(a135.rawScript,  expectScript)
            self.assertEqual(a135.scrAddrStr, expectScrAddr)
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
            self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
            self.assertEqual(a135.lowestUnusedChild, 0)
            self.assertEqual(a135.nextChildToCalc,   0)
         
            kidx += 1
            prevScrAddr = expectScrAddr
            a135 = a135.spawnChild()
         
   
         scrAddrToIndex = {}
         for idx,a135 in a135rt.root135ChainMap.iteritems():
            scrAddrToIndex[a135.getScrAddr()] = idx
            self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
            if idx>0:
               self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
               self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
               self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
               self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)
   
         for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
            self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)


   #############################################################################
   def test135KeyPool(self):
      for WO in [False, True]:
         mockwlt = MockWalletFile()
         seed = SecureBinaryData(self.binSeed)
         a135rt = Armory135Root()
         a135rt.privCryptInfo = NULLCRYPTINFO()
         a135rt.childPoolSize = 5
         a135rt.wltFileRef = mockwlt
         a135rt.initializeFromSeed(seed, fillPool=False)


         self.assertEqual(len(a135rt.akpChildByIndex),   0)
         self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
         self.assertEqual(len(a135rt.root135ChainMap),   0)
         self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
         self.assertEqual(a135rt.rootLowestUnused,       0)
         self.assertEqual(a135rt.rootNextToCalc,         0)

         if WO:
            a135rt.wipePrivateData()

         # Peek at the next addr, confirm root didn't change
         testChild = a135rt.peekNextUnusedChild()
         self.assertEqual(len(a135rt.akpChildByIndex),   0)
         self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
         self.assertEqual(len(a135rt.root135ChainMap),   0)
         self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
         self.assertEqual(a135rt.rootLowestUnused,       0)
         self.assertEqual(a135rt.rootNextToCalc,         0)
         self.assertEqual(testChild.getScrAddr(), self.keyList[0]['ScrAddr'])
         

         a135rt.fillKeyPoolRecurse()

         self.assertEqual(len(a135rt.akpChildByIndex),   1)
         self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
         self.assertEqual(len(a135rt.root135ChainMap),   5)
         self.assertEqual(len(a135rt.root135ScrAddrMap), 5)
         self.assertEqual(a135rt.rootLowestUnused,       0)
         self.assertEqual(a135rt.rootNextToCalc,         5)


         parScrAddr = a135rt.getScrAddr()
         for i,ch in a135rt.root135ChainMap.iteritems():
            kdata = self.keyList[i]
            pub65 = kdata['PubKey']
            a160  = hash160(pub65.toBinStr())
            expectPriv   = kdata['PrivKey'].copy()
            expectPub    = CryptoECDSA().CompressPoint(pub65)
            expectChain  = self.chaincode.copy()
            expectScript = hash160_to_p2pkhash_script(a160)
            expectScrAddr= script_to_scrAddr(expectScript)

            self.assertEqual(expectScrAddr, kdata['ScrAddr'])
            self.assertEqual(expectScrAddr, kdata['ScrAddr'])

            self.assertEqual(ch.isWatchOnly, WO)
            self.assertEqual(ch.sbdPublicKey33, expectPub)
            self.assertEqual(ch.sbdChaincode,   expectChain)
            self.assertEqual(ch.useCompressPub, False)
            self.assertEqual(ch.isUsed, False)
            self.assertEqual(ch.privKeyNextUnlock, False)
            self.assertEqual(ch.akpParScrAddr, parScrAddr)
            self.assertEqual(ch.childIndex, 0)
            self.assertEqual(ch.chainIndex, i)
            self.assertEqual(ch.childPoolSize, 1)
            self.assertEqual(ch.maxChildren, 1)
            self.assertEqual(ch.rawScript,  expectScript)
            self.assertEqual(ch.scrAddrStr, expectScrAddr)
            self.assertEqual(ch.lowestUnusedChild, 0)
            self.assertEqual(ch.nextChildToCalc,   1 if i<4 else 0)

            
            if i>0:
               # These checks look redundant, but are making sure all the refs
               # are set properly between root, parent, child
               par = a135rt.root135ChainMap[i-1]
               self.assertEqual(par.akpChildByIndex[0].getScrAddr(), expectScrAddr)
               self.assertEqual(ch.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
               self.assertEqual(a135rt.root135ChainMap[i].getScrAddr(), expectScrAddr)
               self.assertEqual(ch.akpRootRef.root135ChainMap[i].getScrAddr(), expectScrAddr)
               self.assertTrue(expectScrAddr in par.akpChildByScrAddr)
               self.assertTrue(expectScrAddr in a135rt.root135ScrAddrMap)

            parScrAddr = expectScrAddr



         
         a135rt.rootLowestUnused += 2
         a135rt.fillKeyPoolRecurse()

         self.assertEqual(len(a135rt.akpChildByIndex),   1)
         self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
         self.assertEqual(len(a135rt.root135ChainMap),   7)
         self.assertEqual(len(a135rt.root135ScrAddrMap), 7)
         self.assertEqual(a135rt.rootLowestUnused,       2)
         self.assertEqual(a135rt.rootNextToCalc,         7)



   #############################################################################
   def testGetNextUnused(self):
      for WO in [False, True]:
         POOLSZ = 3
         mockwlt = MockWalletFile()
         seed = SecureBinaryData(self.binSeed)
         a135rt = Armory135Root()
         a135rt.privCryptInfo = NULLCRYPTINFO()
         a135rt.childPoolSize = POOLSZ
         a135rt.wltFileRef = mockwlt
         a135rt.initializeFromSeed(seed, fillPool=False)

         self.assertEqual(len(a135rt.akpChildByIndex),   0)
         self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
         self.assertEqual(len(a135rt.root135ChainMap),   0)
         self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
         self.assertEqual(a135rt.rootLowestUnused,       0)
         self.assertEqual(a135rt.rootNextToCalc,         0)

         if WO:
            a135rt.wipePrivateData()

         kidx = 0
         prevScrAddr = a135rt.getScrAddr()
         rootScrAddr = a135rt.getScrAddr()

         #a135rt.pprintVerbose()

         while kidx+3 in self.keyList:
            #print '---Testing k =', kidx
   
            # This calls fillKeyPoolRecurse, so the keypool is always +3
            a135 = a135rt.getNextUnusedChild()
            #a135rt.pprintVerbose()
            self.assertEqual(len(a135rt.root135ChainMap), kidx+POOLSZ+1)
            self.assertEqual(len(a135rt.root135ScrAddrMap), kidx+POOLSZ+1)
            self.assertEqual(a135rt.rootLowestUnused, kidx+1)
            self.assertEqual(a135rt.rootNextToCalc, kidx+POOLSZ+1)

            pub65 = self.keyList[kidx]['PubKey']
            a160  = hash160(pub65.toBinStr())
   
            expectPriv   = self.keyList[kidx]['PrivKey'].copy()
            expectPub    = CryptoECDSA().CompressPoint(pub65)
            expectChain  = self.chaincode.copy()
            expectScript = hash160_to_p2pkhash_script(a160)
            expectScrAddr= script_to_scrAddr(expectScript)
            self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

            if not WO:
               self.assertEqual(a135.sbdPrivKeyData, expectPriv)
               self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)
            else:
               self.assertEqual(a135.sbdPrivKeyData, NULLSBD())
   
            self.assertEqual(a135.isWatchOnly, WO)
            self.assertEqual(a135.sbdPublicKey33, expectPub)
            self.assertEqual(a135.sbdChaincode,   expectChain)
            self.assertEqual(a135.useCompressPub, False)
            self.assertEqual(a135.isUsed, True)
            self.assertEqual(a135.privKeyNextUnlock, False)
            self.assertEqual(a135.akpParScrAddr, prevScrAddr)
            self.assertEqual(a135.childIndex, 0)
            self.assertEqual(a135.childPoolSize, 1)
            self.assertEqual(a135.maxChildren, 1)
            self.assertEqual(a135.rawScript,  expectScript)
            self.assertEqual(a135.scrAddrStr, expectScrAddr)
            self.assertEqual(a135.lowestUnusedChild, 0)
            self.assertEqual(a135.nextChildToCalc,   1)

            self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)

         
            kidx += 1
            prevScrAddr = expectScrAddr
         
   
         scrAddrToIndex = {}
         for idx,a135 in a135rt.root135ChainMap.iteritems():
            #print 'Testing,  %d:%s' % (idx,binary_to_hex(a135.getScrAddr()))
            scrAddrToIndex[a135.getScrAddr()] = idx
            self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
            if idx>0:
               self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
               self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
               self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
               self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)
   
         for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
            self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)
      


################################################################################
################################################################################
#
# Armory 135 TESTS  (WITH ENCRYPTION)
#
# Most tests are nearly identical to the previous set of 135 tests, except
# using encrypted-but-always-unlocked private keys.  There was probably a way
# to combine these...
#
################################################################################
################################################################################

class A135_Encrypt_Tests(unittest.TestCase):

   #############################################################################
   def setUp(self):
      pass

      self.rootID    = 'zrPzapKR'
      self.rootLine1 = 'okkn weod aajf skrs jdrj rafa gjtr saho eari'.replace(' ','')
      self.rootLine2 = 'rdeg jaah soea ugas jeot niua jdeg hkou gsih'.replace(' ','')
      self.binSeed   = readSixteenEasyBytes(self.rootLine1)[0] + \
                       readSixteenEasyBytes(self.rootLine2)[0]
      self.chaincode = DeriveChaincodeFromRootKey_135(SecureBinaryData(self.binSeed))


      self.keyList = {}

      self.keyList[0] = { \
         'AddrStr': '13QVfpnE7TWAnkGGpHak1Z9cJVQWTZrYqb',
         'PrivB58': '5JWFgYDRyCqxMcXprSf84RAfPC4p6x2eifXxNwHuqeL137JC11A',
         'PubKeyX': '1a84426c38a0099975d683365436ee3eedaf2c9589c44635aa3808ede5f87081',
         'PubKeyY': '6a905e1f3055c0982307951e5e4150349c5c98a644f3da9aeef9c80f103cf2af' }
      self.keyList[1] = { \
         'AddrStr': '1Dy4cGbv3KKm4EhQYVKvUJQfy6sgmGR4ii',
         'PrivB58': '5KMBzjqDE8dXxtvRaY8dGHnMUNyE6uonDwKgeG44XBsngqTYkf9',
         'PubKeyX': '6c23cc6208a1f6daaa196ba6e763b445555ada6315ebf9465a0b9cb49e813e3a',
         'PubKeyY': '341eb33ed738b6a1ac6a57526a80af2e6841dcf71f287dbe721dd4486d9cf8c4' }
      self.keyList[2] = { \
         'AddrStr': '1BKG36rBdxiYNRQbLCYfPzi6Cf4pW2aRxQ',
         'PrivB58': '5KhpN6mmdiVcKmZtPjqfC41Af7181Dj4JadyU7dDLVefdPcMbZi',
         'PubKeyX': 'eb013f8047ad532a8bcc4d4f69a62887ce82afb574d7fb8a326b9bab82d240fa',
         'PubKeyY': 'a8fdcd604105292cb04c7707da5e42300bc418654f8ffc94e2c83bd5a54e09e2' }
      self.keyList[3] = { \
         'AddrStr': '1NhZfoXMLmohuvAh7Ks67JMx6mpcVq2FCa',
         'PrivB58': '5KaxXWwQgFcp3d5Bqd58xvtBDN8FEPQeRZJDpyxY5LTZ5ALZHE3',
         'PubKeyX': 'd6e6d3031d5d3de48293d97590f5b697089e8e6b40e919a68e2a07c300c1256b',
         'PubKeyY': '3d9b428e0ef9f73bd81c9388e1d8702f477138ca444eed57370d0e31ba9bafe5' }
      self.keyList[4] = { \
         'AddrStr': '1GHvHhrUBL5mMryscJa9uzDnPXeEpqU7Tn',
         'PrivB58': '5Jb4u9bpWDv19y6hu6nAE7cDdQoUrJMoyrwGDjPxMKo8oxULSdn',
         'PubKeyX': 'e40d3923bfffad0cdc6d6a3341c8e669beb1264b86cbfd21229ca8a74cf53ca5',
         'PubKeyY': '587b7a9b18b648cd421d17d45d05e8fc647f7ea02f61b670a2d4c2012e3b717f' }
      self.keyList[5] = { \
         'AddrStr': '1DdAdN2VQXg52YqDssZ4o6XprVgEB4Evpj',
         'PrivB58': '5JxD9BrDhCgWEKfEUG2FBcAk1D667G97hNREg81M5Qzgi9CAgdD',
         'PubKeyX': '7e043899f917288db2962819cd78c8328efb6dd172b9cbe1bfaaf8d745fd3e99',
         'PubKeyY': '746b29150ff3828556595291419d579c824ac2879d83fb3d51d5efea5de4715d' }
      self.keyList[6] = { \
         'AddrStr': '1K9QBzxv2jL7ftMkJ9jghr8dJgZ6u6zhHR',
         'PrivB58': '5K7GHu48sqxnYNhiMNVVoeh8WXnnerrNhL2TWocHngaP8zyUPAr',
         'PubKeyX': 'bbc9cd69dd6977b08d7916c0da81208df0b8a491b0897ca482bd42df47102d6b',
         'PubKeyY': 'f0318b3298ba93831df82b7ce51da5e0e8647a3ecd994f600a84834b424ed2b8' }

      # For reference, here's the first 6 ScrAddrs
      # ROOT: 00ef2ba030696d99d945fea3990e4213c62d042ddd
      # 0: 001a61c02c74328db5122fa9c1d4917f05de86a8c2
      # 1: 008e3bd0ad4a85b3fd3d4998397e8da93635aab664
      # 2: 0071254bf82804253fbafaf49b45fe7f85eba0d3d5
      # 3: 00ee068cf6c7b6fc77326cba37d621aebe834a5257
      # 4: 00a7bd0654e2bebf43acfab6b75a4619e70464cce8
      # 5: 008a78852b767f5b5dc8567dbfa53214e914430789

      self.password = SecureBinaryData('hello')
      master32 = SecureBinaryData('\x3e'*32)
      randomiv = SecureBinaryData('\x7d'*8)
      # Create a KDF to be used for encryption key password
      self.kdf = KdfObject('ROMIXOV2', memReqd=32*KILOBYTE,
                                       numIter=1, 
                                       salt=SecureBinaryData('\x21'*32))

      # Create the new master encryption key to be used to encrypt priv keys
      self.ekey = EncryptionKey().createNewMasterKey(self.kdf, 'AE256CBC', 
                     self.password, preGenKey=master32, preGenIV8=randomiv)

      # This will be attached to each ABEK object, to define its encryption
      self.privACI = ArmoryCryptInfo(NULLKDF, 'AE256CBC', 
                                 self.ekey.ekeyID, 'PUBKEY20')

      self.ekey.unlock(self.password)
      for idx,imap in self.keyList.iteritems():
         imap['PrivKey']   = SecureBinaryData(parsePrivateKeyData(imap['PrivB58'])[0])
         imap['PubKey']    = SecureBinaryData(hex_to_binary('04' + imap['PubKeyX'] + imap['PubKeyY']))
         imap['Chaincode'] = self.chaincode.copy()
         imap['ScrAddr']   = SCRADDR_P2PKH_BYTE + hash160(imap['PubKey'].toBinStr())

         # Compute encrypted version of privkey with associated (compr) pubkey
         pub33 = CryptoECDSA().CompressPoint(imap['PubKey'])
         iv = SecureBinaryData(hash256(pub33.toBinStr())[:16])
         imap['PrivCrypt'] = self.privACI.encrypt(imap['PrivKey'], ekeyObj=self.ekey, ivData=iv)
      self.ekey.lock()
      
   #############################################################################
   def tearDown(self):
      pass
      

   #############################################################################
   def testInitFromSeed_Crypt(self):
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = 3

      self.assertRaises(WalletLockError, a135rt.initializeFromSeed, seed, fillPool=False)

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)

      self.assertEqual(a135rt.sbdSeedData.toHexStr(), '') # supposed to be empty
      self.assertEqual(a135rt.privCryptInfo.serialize(), self.privACI.serialize())
      self.assertEqual(a135rt.privKeyNextUnlock, False)

      self.assertEqual(a135rt.getPlainSeedCopy().toHexStr(), seed.toHexStr())
      self.assertEqual(a135rt.getUniqueIDB58(), self.rootID)

      self.assertEqual(a135rt.rootLowestUnused, 0)
      self.assertEqual(a135rt.rootNextToCalc,   0)



   #############################################################################
   def testSpawnA135_Crypt(self):

      a135 = Armory135KeyPair()
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = 3
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)


      self.ekey.lock(self.password)
      self.assertRaises(WalletLockError, a135rt.spawnChild, privSpawnReqd=True)

      self.ekey.unlock(self.password)
      a135 = a135rt.spawnChild()
      self.assertEqual(a135rt.rootLowestUnused, 0)
      self.assertEqual(a135rt.rootNextToCalc,   1)

      prevScrAddr = a135rt.getScrAddr()
      rootScrAddr = a135rt.getScrAddr()

      kidx = 0
      while kidx+1 in self.keyList:

         pub65 = self.keyList[kidx]['PubKey']
         a160  = hash160(pub65.toBinStr())

         expectPriv   = self.keyList[kidx]['PrivKey'].copy()
         expectCrypt  = self.keyList[kidx]['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)
         self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

         self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
         self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)

         self.assertEqual(a135.isWatchOnly, False)
         self.assertEqual(a135.sbdPublicKey33, expectPub)
         self.assertEqual(a135.sbdChaincode,   expectChain)
         self.assertEqual(a135.useCompressPub, False)
         self.assertEqual(a135.isUsed, False)
         self.assertEqual(a135.privKeyNextUnlock, False)
         self.assertEqual(a135.akpParScrAddr, prevScrAddr)
         self.assertEqual(a135.childIndex, 0)
         self.assertEqual(a135.childPoolSize, 1)
         self.assertEqual(a135.maxChildren, 1)
         self.assertEqual(a135.rawScript,  expectScript)
         self.assertEqual(a135.scrAddrStr, expectScrAddr)
         self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.lowestUnusedChild, 0)
         self.assertEqual(a135.nextChildToCalc,   0)
      
         kidx += 1
         prevScrAddr = expectScrAddr
         a135 = a135.spawnChild()
      

      scrAddrToIndex = {}
      for idx,a135 in a135rt.root135ChainMap.iteritems():
         scrAddrToIndex[a135.getScrAddr()] = idx
         self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
         if idx>0:
            self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
            self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
            self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)

      for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
         self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)


   #############################################################################
   def test135KeyPool_Crypt(self):
      a135 = Armory135KeyPair()
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = 5
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)


      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)


      # Peek at the next addr, confirm root didn't change
      testChild = a135rt.peekNextUnusedChild()
      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)
      self.assertEqual(testChild.getScrAddr(), self.keyList[0]['ScrAddr'])
      

      a135rt.fillKeyPoolRecurse()

      self.assertEqual(len(a135rt.akpChildByIndex),   1)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
      self.assertEqual(len(a135rt.root135ChainMap),   5)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 5)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         5)


      parScrAddr = a135rt.getScrAddr()
      for i,ch in a135rt.root135ChainMap.iteritems():
         kdata = self.keyList[i]
         pub65 = kdata['PubKey']
         a160  = hash160(pub65.toBinStr())
         expectPriv   = kdata['PrivKey'].copy()
         expectCrypt  = kdata['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)

         self.assertEqual(expectScrAddr, kdata['ScrAddr'])
         self.assertEqual(expectScrAddr, kdata['ScrAddr'])

         self.assertEqual(ch.isWatchOnly, False)
         self.assertEqual(ch.sbdPrivKeyData, expectCrypt)
         self.assertEqual(ch.getPlainPrivKeyCopy(), expectPriv)
         self.assertEqual(ch.sbdPublicKey33, expectPub)
         self.assertEqual(ch.sbdChaincode,   expectChain)
         self.assertEqual(ch.useCompressPub, False)
         self.assertEqual(ch.isUsed, False)
         self.assertEqual(ch.privKeyNextUnlock, False)
         self.assertEqual(ch.akpParScrAddr, parScrAddr)
         self.assertEqual(ch.childIndex, 0)
         self.assertEqual(ch.chainIndex, i)
         self.assertEqual(ch.childPoolSize, 1)
         self.assertEqual(ch.maxChildren, 1)
         self.assertEqual(ch.rawScript,  expectScript)
         self.assertEqual(ch.scrAddrStr, expectScrAddr)
         self.assertEqual(ch.lowestUnusedChild, 0)
         self.assertEqual(ch.nextChildToCalc,   1 if i<4 else 0)

         
         if i>0:
            # These checks look redundant, but are making sure all the refs
            # are set properly between root, parent, child
            par = a135rt.root135ChainMap[i-1]
            self.assertEqual(par.akpChildByIndex[0].getScrAddr(), expectScrAddr)
            self.assertEqual(ch.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
            self.assertEqual(a135rt.root135ChainMap[i].getScrAddr(), expectScrAddr)
            self.assertEqual(ch.akpRootRef.root135ChainMap[i].getScrAddr(), expectScrAddr)
            self.assertTrue(expectScrAddr in par.akpChildByScrAddr)
            self.assertTrue(expectScrAddr in a135rt.root135ScrAddrMap)

         parScrAddr = expectScrAddr



      
      a135rt.rootLowestUnused += 2
      a135rt.fillKeyPoolRecurse()

      self.assertEqual(len(a135rt.akpChildByIndex),   1)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
      self.assertEqual(len(a135rt.root135ChainMap),   7)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 7)
      self.assertEqual(a135rt.rootLowestUnused,       2)
      self.assertEqual(a135rt.rootNextToCalc,         7)



   #############################################################################
   def testGetNextUnused_Crypt(self):
      POOLSZ = 3
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)
      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = POOLSZ
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)

      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)


      kidx = 0
      prevScrAddr = a135rt.getScrAddr()
      rootScrAddr = a135rt.getScrAddr()

      #a135rt.pprintVerbose()

      while kidx+3 in self.keyList:
         #print '---Testing k =', kidx

         # This calls fillKeyPoolRecurse, so the keypool is always +3
         a135 = a135rt.getNextUnusedChild()
         #a135rt.pprintVerbose()
         self.assertEqual(len(a135rt.root135ChainMap), kidx+POOLSZ+1)
         self.assertEqual(len(a135rt.root135ScrAddrMap), kidx+POOLSZ+1)
         self.assertEqual(a135rt.rootLowestUnused, kidx+1)
         self.assertEqual(a135rt.rootNextToCalc, kidx+POOLSZ+1)

         pub65 = self.keyList[kidx]['PubKey']
         a160  = hash160(pub65.toBinStr())

         expectPriv   = self.keyList[kidx]['PrivKey'].copy()
         expectCrypt  = self.keyList[kidx]['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)
         self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

         self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
         self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)

         self.assertEqual(a135.isWatchOnly, False)
         self.assertEqual(a135.sbdPublicKey33, expectPub)
         self.assertEqual(a135.sbdChaincode,   expectChain)
         self.assertEqual(a135.useCompressPub, False)
         self.assertEqual(a135.isUsed, True)
         self.assertEqual(a135.privKeyNextUnlock, False)
         self.assertEqual(a135.akpParScrAddr, prevScrAddr)
         self.assertEqual(a135.childIndex, 0)
         self.assertEqual(a135.childPoolSize, 1)
         self.assertEqual(a135.maxChildren, 1)
         self.assertEqual(a135.rawScript,  expectScript)
         self.assertEqual(a135.scrAddrStr, expectScrAddr)
         self.assertEqual(a135.lowestUnusedChild, 0)
         self.assertEqual(a135.nextChildToCalc,   1)

         self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)

      
         kidx += 1
         prevScrAddr = expectScrAddr
      

      scrAddrToIndex = {}
      for idx,a135 in a135rt.root135ChainMap.iteritems():
         #print 'Testing,  %d:%s' % (idx,binary_to_hex(a135.getScrAddr()))
         scrAddrToIndex[a135.getScrAddr()] = idx
         self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
         if idx>0:
            self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
            self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
            self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)

      for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
         self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)

      
################################################################################
################################################################################
#
# Armory 135 NEXTUNLOCK TESTS
#
################################################################################
################################################################################

class A135_NextUnlock_Tests(unittest.TestCase):

   #############################################################################
   def setUp(self):
      pass

      self.rootID    = 'zrPzapKR'
      self.rootLine1 = 'okkn weod aajf skrs jdrj rafa gjtr saho eari'.replace(' ','')
      self.rootLine2 = 'rdeg jaah soea ugas jeot niua jdeg hkou gsih'.replace(' ','')
      self.binSeed   = readSixteenEasyBytes(self.rootLine1)[0] + \
                       readSixteenEasyBytes(self.rootLine2)[0]
      self.chaincode = DeriveChaincodeFromRootKey_135(SecureBinaryData(self.binSeed))


      self.keyList = {}

      self.keyList[0] = { \
         'AddrStr': '13QVfpnE7TWAnkGGpHak1Z9cJVQWTZrYqb',
         'PrivB58': '5JWFgYDRyCqxMcXprSf84RAfPC4p6x2eifXxNwHuqeL137JC11A',
         'PubKeyX': '1a84426c38a0099975d683365436ee3eedaf2c9589c44635aa3808ede5f87081',
         'PubKeyY': '6a905e1f3055c0982307951e5e4150349c5c98a644f3da9aeef9c80f103cf2af' }
      self.keyList[1] = { \
         'AddrStr': '1Dy4cGbv3KKm4EhQYVKvUJQfy6sgmGR4ii',
         'PrivB58': '5KMBzjqDE8dXxtvRaY8dGHnMUNyE6uonDwKgeG44XBsngqTYkf9',
         'PubKeyX': '6c23cc6208a1f6daaa196ba6e763b445555ada6315ebf9465a0b9cb49e813e3a',
         'PubKeyY': '341eb33ed738b6a1ac6a57526a80af2e6841dcf71f287dbe721dd4486d9cf8c4' }
      self.keyList[2] = { \
         'AddrStr': '1BKG36rBdxiYNRQbLCYfPzi6Cf4pW2aRxQ',
         'PrivB58': '5KhpN6mmdiVcKmZtPjqfC41Af7181Dj4JadyU7dDLVefdPcMbZi',
         'PubKeyX': 'eb013f8047ad532a8bcc4d4f69a62887ce82afb574d7fb8a326b9bab82d240fa',
         'PubKeyY': 'a8fdcd604105292cb04c7707da5e42300bc418654f8ffc94e2c83bd5a54e09e2' }
      self.keyList[3] = { \
         'AddrStr': '1NhZfoXMLmohuvAh7Ks67JMx6mpcVq2FCa',
         'PrivB58': '5KaxXWwQgFcp3d5Bqd58xvtBDN8FEPQeRZJDpyxY5LTZ5ALZHE3',
         'PubKeyX': 'd6e6d3031d5d3de48293d97590f5b697089e8e6b40e919a68e2a07c300c1256b',
         'PubKeyY': '3d9b428e0ef9f73bd81c9388e1d8702f477138ca444eed57370d0e31ba9bafe5' }
      self.keyList[4] = { \
         'AddrStr': '1GHvHhrUBL5mMryscJa9uzDnPXeEpqU7Tn',
         'PrivB58': '5Jb4u9bpWDv19y6hu6nAE7cDdQoUrJMoyrwGDjPxMKo8oxULSdn',
         'PubKeyX': 'e40d3923bfffad0cdc6d6a3341c8e669beb1264b86cbfd21229ca8a74cf53ca5',
         'PubKeyY': '587b7a9b18b648cd421d17d45d05e8fc647f7ea02f61b670a2d4c2012e3b717f' }
      self.keyList[5] = { \
         'AddrStr': '1DdAdN2VQXg52YqDssZ4o6XprVgEB4Evpj',
         'PrivB58': '5JxD9BrDhCgWEKfEUG2FBcAk1D667G97hNREg81M5Qzgi9CAgdD',
         'PubKeyX': '7e043899f917288db2962819cd78c8328efb6dd172b9cbe1bfaaf8d745fd3e99',
         'PubKeyY': '746b29150ff3828556595291419d579c824ac2879d83fb3d51d5efea5de4715d' }
      self.keyList[6] = { \
         'AddrStr': '1K9QBzxv2jL7ftMkJ9jghr8dJgZ6u6zhHR',
         'PrivB58': '5K7GHu48sqxnYNhiMNVVoeh8WXnnerrNhL2TWocHngaP8zyUPAr',
         'PubKeyX': 'bbc9cd69dd6977b08d7916c0da81208df0b8a491b0897ca482bd42df47102d6b',
         'PubKeyY': 'f0318b3298ba93831df82b7ce51da5e0e8647a3ecd994f600a84834b424ed2b8' }

      # For reference, here's the first 6 ScrAddrs
      # ROOT: 00ef2ba030696d99d945fea3990e4213c62d042ddd
      # 0: 001a61c02c74328db5122fa9c1d4917f05de86a8c2
      # 1: 008e3bd0ad4a85b3fd3d4998397e8da93635aab664
      # 2: 0071254bf82804253fbafaf49b45fe7f85eba0d3d5
      # 3: 00ee068cf6c7b6fc77326cba37d621aebe834a5257
      # 4: 00a7bd0654e2bebf43acfab6b75a4619e70464cce8
      # 5: 008a78852b767f5b5dc8567dbfa53214e914430789

      self.password = SecureBinaryData('hello')
      master32 = SecureBinaryData('\x3e'*32)
      randomiv = SecureBinaryData('\x7d'*8)
      # Create a KDF to be used for encryption key password
      self.kdf = KdfObject('ROMIXOV2', memReqd=32*KILOBYTE,
                                       numIter=1, 
                                       salt=SecureBinaryData('\x21'*32))

      # Create the new master encryption key to be used to encrypt priv keys
      self.ekey = EncryptionKey().createNewMasterKey(self.kdf, 'AE256CBC', 
                     self.password, preGenKey=master32, preGenIV8=randomiv)

      # This will be attached to each ABEK object, to define its encryption
      self.privACI = ArmoryCryptInfo(NULLKDF, 'AE256CBC', 
                                 self.ekey.ekeyID, 'PUBKEY20')

      self.ekey.unlock(self.password)
      for idx,imap in self.keyList.iteritems():
         imap['PrivKey']   = SecureBinaryData(parsePrivateKeyData(imap['PrivB58'])[0])
         imap['PubKey']    = SecureBinaryData(hex_to_binary('04' + imap['PubKeyX'] + imap['PubKeyY']))
         imap['Chaincode'] = self.chaincode.copy()
         imap['ScrAddr']   = SCRADDR_P2PKH_BYTE + hash160(imap['PubKey'].toBinStr())

         # Compute encrypted version of privkey with associated (compr) pubkey
         pub33 = CryptoECDSA().CompressPoint(imap['PubKey'])
         iv = SecureBinaryData(hash256(pub33.toBinStr())[:16])
         imap['PrivCrypt'] = self.privACI.encrypt(imap['PrivKey'], ekeyObj=self.ekey, ivData=iv)
      self.ekey.lock()


      
   #############################################################################
   def tearDown(self):
      pass
      



   #############################################################################
   def testSpawnA135_ResolveNextUnlock(self):
      """
      This test is going to create an artificial chain of 135 keys, with 
      the nextUnlock flags set to True, then attempt to resolve it.  Later 
      we will create naturally-occurring nextUnlock structures to test resolving
      """
      POOLSZ = 3
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)
      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = POOLSZ
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)

      a135 = a135rt.spawnChild() 
      a135List = []
      kidx = 0
      while kidx in self.keyList:

         pub65 = self.keyList[kidx]['PubKey']
         a160  = hash160(pub65.toBinStr())
         expectPriv   = self.keyList[kidx]['PrivKey'].copy()
         expectCrypt  = self.keyList[kidx]['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)
         self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

         self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
         self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)
         self.assertEqual(a135.isWatchOnly, False)
         self.assertEqual(a135.sbdPublicKey33, expectPub)
         self.assertEqual(a135.sbdChaincode,   expectChain)
         self.assertEqual(a135.useCompressPub, False)
         self.assertEqual(a135.isUsed, False)
         self.assertEqual(a135.privKeyNextUnlock, False)
         self.assertEqual(a135.rawScript,  expectScript)
         self.assertEqual(a135.scrAddrStr, expectScrAddr)
      
         kidx += 1
         a135List.append(a135)
         a135 = a135.spawnChild()


      # Okay, the above was just setup an verification of the setup
      # Now we delete the encrypted priv key data and try resolving from var points
      def resetTest(keyWipeList):
         for i,kmap in self.keyList.iteritems():
            if i in keyWipeList:
               a135List[i].sbdPrivKeyData.destroy()
               a135List[i].privKeyNextUnlock = True
            else:
               a135List[i].sbdPrivKeyData = kmap['PrivCrypt'].copy()
               a135List[i].privKeyNextUnlock = False


      def printResolveList():
         print 'Reset List:'
         for a in a135List:
            print a.chainIndex, a.privKeyNextUnlock, a.sbdPrivKeyData.getSize()

      def testResolveAndCheck(idx):
         a135List[idx].resolveNextUnlockFlag()
         for i,a135 in enumerate(a135List):
            if i<=idx:
               expectCrypt  = self.keyList[i]['PrivCrypt'].copy()
               expectPubKey = self.keyList[i]['PubKey'].copy()
               expectChain  = a135rt.sbdChaincode.copy()
               expectUnlock  = False
            else:
               expectCrypt  = NULLSBD()
               expectPubKey = self.keyList[i]['PubKey'].copy()
               expectChain  = a135rt.sbdChaincode.copy()
               expectUnlock = True

            expectPubKey = CryptoECDSA().CompressPoint(expectPubKey)
            self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
            self.assertEqual(a135.sbdPublicKey33, expectPubKey)
            self.assertEqual(a135.sbdChaincode,   expectChain)
            self.assertEqual(a135.privKeyNextUnlock, expectUnlock)

      self.ekey.unlock(self.password)

      resetTest(range(7))
      testResolveAndCheck(0)

      resetTest(range(7))
      testResolveAndCheck(1)

      resetTest(range(7))
      testResolveAndCheck(6)

      resetTest([4,5,6])
      testResolveAndCheck(5)

      resetTest([4,5,6])
      testResolveAndCheck(6)

   '''
   #############################################################################
   def testSpawnA135_NextUnlock(self):

      a135 = Armory135KeyPair()
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = 3
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)


      self.ekey.lock(self.password)
      self.assertRaises(WalletLockError, a135rt.spawnChild, privSpawnReqd=True)

      self.ekey.unlock(self.password)
      a135 = a135rt.spawnChild()
      self.assertEqual(a135rt.rootLowestUnused, 0)
      self.assertEqual(a135rt.rootNextToCalc,   1)

      prevScrAddr = a135rt.getScrAddr()
      rootScrAddr = a135rt.getScrAddr()

      kidx = 0
      while kidx+1 in self.keyList:

         pub65 = self.keyList[kidx]['PubKey']
         a160  = hash160(pub65.toBinStr())

         expectPriv   = self.keyList[kidx]['PrivKey'].copy()
         expectCrypt  = self.keyList[kidx]['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)
         self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

         self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
         self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)

         self.assertEqual(a135.isWatchOnly, False)
         self.assertEqual(a135.sbdPublicKey33, expectPub)
         self.assertEqual(a135.sbdChaincode,   expectChain)
         self.assertEqual(a135.useCompressPub, False)
         self.assertEqual(a135.isUsed, False)
         self.assertEqual(a135.privKeyNextUnlock, False)
         self.assertEqual(a135.akpParScrAddr, prevScrAddr)
         self.assertEqual(a135.childIndex, 0)
         self.assertEqual(a135.childPoolSize, 1)
         self.assertEqual(a135.maxChildren, 1)
         self.assertEqual(a135.rawScript,  expectScript)
         self.assertEqual(a135.scrAddrStr, expectScrAddr)
         self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.lowestUnusedChild, 0)
         self.assertEqual(a135.nextChildToCalc,   0)
      
         kidx += 1
         prevScrAddr = expectScrAddr
         a135 = a135.spawnChild()
      

      scrAddrToIndex = {}
      for idx,a135 in a135rt.root135ChainMap.iteritems():
         scrAddrToIndex[a135.getScrAddr()] = idx
         self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
         if idx>0:
            self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
            self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
            self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)

      for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
         self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)


   #############################################################################
   def test135KeyPool_NextUnlock(self):
      a135 = Armory135KeyPair()
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)

      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = 5
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)


      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)


      # Peek at the next addr, confirm root didn't change
      testChild = a135rt.peekNextUnusedChild()
      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)
      self.assertEqual(testChild.getScrAddr(), self.keyList[0]['ScrAddr'])
      

      a135rt.fillKeyPoolRecurse()

      self.assertEqual(len(a135rt.akpChildByIndex),   1)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
      self.assertEqual(len(a135rt.root135ChainMap),   5)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 5)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         5)


      parScrAddr = a135rt.getScrAddr()
      for i,ch in a135rt.root135ChainMap.iteritems():
         kdata = self.keyList[i]
         pub65 = kdata['PubKey']
         a160  = hash160(pub65.toBinStr())
         expectPriv   = kdata['PrivKey'].copy()
         expectCrypt  = kdata['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)

         self.assertEqual(expectScrAddr, kdata['ScrAddr'])
         self.assertEqual(expectScrAddr, kdata['ScrAddr'])

         self.assertEqual(ch.isWatchOnly, False)
         self.assertEqual(ch.sbdPrivKeyData, expectCrypt)
         self.assertEqual(ch.getPlainPrivKeyCopy(), expectPriv)
         self.assertEqual(ch.sbdPublicKey33, expectPub)
         self.assertEqual(ch.sbdChaincode,   expectChain)
         self.assertEqual(ch.useCompressPub, False)
         self.assertEqual(ch.isUsed, False)
         self.assertEqual(ch.privKeyNextUnlock, False)
         self.assertEqual(ch.akpParScrAddr, parScrAddr)
         self.assertEqual(ch.childIndex, 0)
         self.assertEqual(ch.chainIndex, i)
         self.assertEqual(ch.childPoolSize, 1)
         self.assertEqual(ch.maxChildren, 1)
         self.assertEqual(ch.rawScript,  expectScript)
         self.assertEqual(ch.scrAddrStr, expectScrAddr)
         self.assertEqual(ch.lowestUnusedChild, 0)
         self.assertEqual(ch.nextChildToCalc,   1 if i<4 else 0)

         
         if i>0:
            # These checks look redundant, but are making sure all the refs
            # are set properly between root, parent, child
            par = a135rt.root135ChainMap[i-1]
            self.assertEqual(par.akpChildByIndex[0].getScrAddr(), expectScrAddr)
            self.assertEqual(ch.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)
            self.assertEqual(a135rt.root135ChainMap[i].getScrAddr(), expectScrAddr)
            self.assertEqual(ch.akpRootRef.root135ChainMap[i].getScrAddr(), expectScrAddr)
            self.assertTrue(expectScrAddr in par.akpChildByScrAddr)
            self.assertTrue(expectScrAddr in a135rt.root135ScrAddrMap)

         parScrAddr = expectScrAddr



      
      a135rt.rootLowestUnused += 2
      a135rt.fillKeyPoolRecurse()

      self.assertEqual(len(a135rt.akpChildByIndex),   1)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 1)
      self.assertEqual(len(a135rt.root135ChainMap),   7)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 7)
      self.assertEqual(a135rt.rootLowestUnused,       2)
      self.assertEqual(a135rt.rootNextToCalc,         7)



   #############################################################################
   def testGetNextUnused_NextUnlock(self):
      POOLSZ = 3
      mockwlt = MockWalletFile()
      seed = SecureBinaryData(self.binSeed)
      a135rt = Armory135Root()
      a135rt.privCryptInfo = self.privACI
      a135rt.masterEkeyRef = self.ekey
      a135rt.childPoolSize = POOLSZ
      a135rt.wltFileRef = mockwlt

      self.ekey.unlock(self.password)
      a135rt.initializeFromSeed(seed, fillPool=False)

      self.assertEqual(len(a135rt.akpChildByIndex),   0)
      self.assertEqual(len(a135rt.akpChildByScrAddr), 0)
      self.assertEqual(len(a135rt.root135ChainMap),   0)
      self.assertEqual(len(a135rt.root135ScrAddrMap), 0)
      self.assertEqual(a135rt.rootLowestUnused,       0)
      self.assertEqual(a135rt.rootNextToCalc,         0)


      kidx = 0
      prevScrAddr = a135rt.getScrAddr()
      rootScrAddr = a135rt.getScrAddr()

      #a135rt.pprintVerbose()

      while kidx+3 in self.keyList:
         #print '---Testing k =', kidx

         # This calls fillKeyPoolRecurse, so the keypool is always +3
         a135 = a135rt.getNextUnusedChild()
         #a135rt.pprintVerbose()
         self.assertEqual(len(a135rt.root135ChainMap), kidx+POOLSZ+1)
         self.assertEqual(len(a135rt.root135ScrAddrMap), kidx+POOLSZ+1)
         self.assertEqual(a135rt.rootLowestUnused, kidx+1)
         self.assertEqual(a135rt.rootNextToCalc, kidx+POOLSZ+1)

         pub65 = self.keyList[kidx]['PubKey']
         a160  = hash160(pub65.toBinStr())

         expectPriv   = self.keyList[kidx]['PrivKey'].copy()
         expectCrypt  = self.keyList[kidx]['PrivCrypt'].copy()
         expectPub    = CryptoECDSA().CompressPoint(pub65)
         expectChain  = self.chaincode.copy()
         expectScript = hash160_to_p2pkhash_script(a160)
         expectScrAddr= script_to_scrAddr(expectScript)
         self.assertEqual(expectScrAddr, self.keyList[kidx]['ScrAddr'])

         self.assertEqual(a135.sbdPrivKeyData, expectCrypt)
         self.assertEqual(a135.getPlainPrivKeyCopy(), expectPriv)

         self.assertEqual(a135.isWatchOnly, False)
         self.assertEqual(a135.sbdPublicKey33, expectPub)
         self.assertEqual(a135.sbdChaincode,   expectChain)
         self.assertEqual(a135.useCompressPub, False)
         self.assertEqual(a135.isUsed, True)
         self.assertEqual(a135.privKeyNextUnlock, False)
         self.assertEqual(a135.akpParScrAddr, prevScrAddr)
         self.assertEqual(a135.childIndex, 0)
         self.assertEqual(a135.childPoolSize, 1)
         self.assertEqual(a135.maxChildren, 1)
         self.assertEqual(a135.rawScript,  expectScript)
         self.assertEqual(a135.scrAddrStr, expectScrAddr)
         self.assertEqual(a135.lowestUnusedChild, 0)
         self.assertEqual(a135.nextChildToCalc,   1)

         self.assertEqual(a135.akpRootRef.root135ChainMap[kidx].getScrAddr(), expectScrAddr)
         self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), expectScrAddr)

      
         kidx += 1
         prevScrAddr = expectScrAddr
      

      scrAddrToIndex = {}
      for idx,a135 in a135rt.root135ChainMap.iteritems():
         #print 'Testing,  %d:%s' % (idx,binary_to_hex(a135.getScrAddr()))
         scrAddrToIndex[a135.getScrAddr()] = idx
         self.assertEqual(a135.akpRootRef.getScrAddr(), rootScrAddr)
         if idx>0:
            self.assertEqual(a135.akpParentRef.getScrAddr(), self.keyList[idx-1]['ScrAddr'])
            self.assertEqual(a135.akpParentRef.akpChildByIndex[0].getScrAddr(), a135.getScrAddr())
            self.assertEqual(len(a135.akpParentRef.akpChildByIndex), 1)
            self.assertEqual(len(a135.akpParentRef.akpChildByScrAddr), 1)

      for scrAddr,a135 in a135rt.root135ScrAddrMap.iteritems():
         self.assertEqual(scrAddrToIndex[a135.getScrAddr()], a135.chainIndex)
   '''




if __name__ == "__main__":
   unittest.main()














