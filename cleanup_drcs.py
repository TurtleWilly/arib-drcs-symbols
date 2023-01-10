#!/usr/bin/env python3

#
#  Wilhelm/ JPTV.club
#
#  History:
#       1.4 (10-Jan-2022) - Converted filter to command, because Windows is weird.
#       1.3 (02-Aug-2022) - Cleanups
#       1.2 (14-Sep-2021) - Merged workarounds for Windows
#  	1.1 (12-Sep-2021) - Initial version
#

import re
import sys
import os
import argparse

__author__  = 'Wilhelm/ JPTV.club'
__version__ = '1.4'


# /* look up table -- automatically generated -- */
mappings = {
	'063C95566807D5E7B51AB706426BEDF9': '[ｽﾏﾎ]',
	'06CB56043B9C4006BCFBE07CC831FEAF': '[ｽﾋﾟｰｶ]',
	'0895A30733D262AB1F93A708DD58A18D': '濵',
	'12A2C7156DA32FC972B5A451BB87B813': '｟',
	'12AECDEA283E4D07F88B9F2B740E4F86': '⚟',
	'170193C22E22A88904C34F3EC7129DDB': '[PC]',
	'1A0D5448F0C7AD3592867EF1822625D0': '⎚',
	'1A563501AFFBF7F5BAEC350A108D5505': '⚟',
	'1ACF61D411002097CD9E60E60A835A8F': '[ﾌﾟﾚｰﾔｰ]',
	'1E689794776CB5582A1863B4DEE9FEAC': '[ｹｰﾀｲ]',
	'1EC68789194EA34C7A8A0B89F9550B1D': '[ﾏｲｸ]',
	'21574A6257F78156F74EAE5385997277': '⎚',
	'281FC5F4077EA6427747561BC6C60EFA': '葛',
	'2A063EDC4770B3403F060B38166A0D4D': '｟',
	'2EFC3F9CB8EA7F1AF59B0E3919EBAAA9': '[TV]',
	'32DA82DE0FA624C06429973546962AF8': '[ｽﾋﾟｰｶ]',
	'33D4C5243A45503D43FBB858A728664D': '[ｹｰﾀｲ]',
	'35E1950772932B5E0265782CD3D3D260': '☎',
	'37DDA7E42A71CCE52E92AF10433DCD93': '『',
	'37F6ECF37A0A3EF8DFF083CCC8754F81': '♬',
	'38566B372F4C5A1AEAD4EFA20DECD079': '｠',
	'3D1BD145819ECE4A33807CE3A4B1EFAA': '[ｽﾏﾎ]',
	'4C84BD1AF930BE3E0FDC14944B01867D': '祇',
	'516A7B4EB9DE2841903301997E881E9D': '[ｽﾋﾟｰｶ]',
	'52B83336967BAEDFD10FB3C0EB88C205': '珉',
	'54479AA90145B4713134B78D4FB98AA5': '｟',
	'54809FFDE5588F40F754CBF69A28B404': '弴',
	'563E1633D226C10EF4EC80638997E4A9': '『',
	'583134B86E7D90960F64C5B863196978': '➡',
	'5BB8B7731D9473EBD7C842334DFA24F2': '｠',
	'5C31E7978A711D0CA0469B294CB47CA6': '[ｽﾋﾟｰｶ]',
	'5C8022286D3BC941C12E9BBC475255DD': '鷗',
	'62985AEEBAEC69314F03FF9D3080ADA2': '鷗',
	'650C4061157ECBA687E8934164D83A5F': '樋',
	'668EFE227046308AE8E72C016F2EA3D7': '[ﾃｰﾌﾟ]',
	'68FC649B4A57A6103A25DC678FCEC9F4': '[ｹｰﾀｲ]',
	'6D5AA3FF99A144BD5138562787F58590': '[ｹｰﾀｲ]',
	'6E1D2C6D71AE08CE7F4CF64F23D97DF4': '[TV]',
	'6F15F7D4ADD814229942D280A8ACAE40': '☎',
	'6FD7DBAC9AD5D605768457F173A1CBD1': '[TV]',
	'7160F7419CBA7ACDACD23CBEB4834DBE': '｟',
	'7491E4734BF93C5064B077318BC82EC1': '[ｽﾏﾎ]',
	'74D535CA9F47D57FD78234F7019A525E': '⚟',
	'7542BC0875D546542D2435DAA99821BB': '[ｹｰﾀｲ]',
	'762CBC6B6F0F7132973C0F6CEB4141C6': '☎',
	'7778FA83E2DD213935B75951A07FCCAD': '𣝣',
	'7BFEE4DD2D8C5478F86A169EA60AA03D': '[ｹｰﾀｲ]',
	'7CAF343B9E56DC14B775080F944E21FD': '[ｽﾋﾟｰｶ]',
	'804A5BCDCBF1BA977C92D3D58A1CDFE1': '[ｽﾋﾟｰｶ]',
	'83558EE0307101A7D50EC0904F0CEA52': '』',
	'86AED3FE53AD8F629253795C87452FAB': '[ｹｰﾀｲ]',
	'8B6444BE18F269AC615643B26F9E3041': '『',
	'8E5B873AC8E1BF84246B281B3548C2FF': '↴',
	'929CA2E2768BEDD4A812916925F1266B': '[TV]',
	'94FB7BE756372DB6B62E3E0A119083D5': '⚞',
	'953993322785AB4152AC0D3747D7ACF5': '『',
	'97CDEDD3618D1510CC3904D4652F5790': '[ｽﾏﾎ]',
	'9D15C0395A4738936AF34308ACF2D032': '｟',
	'9EE59C7D2C202E0214836A0138F59E24': '』',
	'9FFA7E00CFC7E807A161ADA460B8060C': '｠',
	'A191DCAE8572D65EBB1411F17311076A': '『',
	'A368B4CE2212EF80E2BF3D68559F5151': '⎚',
	'A58DC0E1271B03A5981B57A83271AFA7': '｠',
	'A78D9B65F46654601CE0145622164B47': '↴',
	'A97B575907C06F39C8AC0ED26C49E328': '[ｽﾏﾎ]',
	'AD63C1574C1F4B556B157A0D5FD855FF': '[ｽﾏﾎ]',
	'B1177C2EA37A69B67747287050F28F41': '樋',
	'B84B5D9232B091B461BAA1C07950E76B': '﨑',
	'C01D2BAFCE469DA1ABBB612FDB16C1E3': '元',
	'C08E27670940B3A3DC8122586E144B44': '⎚',
	'C35C7E6816E10BE8304F2D876426C9E7': '[ｹｰﾀｲ]',
	'C42450812C184AEE2AE01CC5E39AE957': '[ﾗｼﾞｵ]',
	'C7A45CD980247B7971BF223F1A71607F': '[PC]',
	'CEF8C8FE116047F9B3214D0DD145EA32': '[CD]',
	'D4F0B6247BBB9102758D1F4A06506C9F': '薩',    
	'DE7F3B9A7048C3A1D5EFE8DEE33953FD': '』',
	'E214599903C94C532684BDF54B62DF61': '｠',
	'E3587F9C5CF08D369D50A459F1D23723': '[TV]',
	'E67210B0DA0161D36B79E8C9BE6A9D0C': '｠',
	'E702912587801D73D58CDB30E48DEBED': '』',
	'E806D1481CFA721DA5F60413531F39BD': '[ｹｰﾀｲ]',
	'F30294B4B8B6C05E9418B1188CE72742': '[ｲｱﾎﾝ]',
	'FBD48A799B4F6802745508A76590E3BC': '[ｹｰﾀｲ]',
	'FE091DA3F60998F83773AEDED2D327DA': '[ｹｰﾀｲ]',	
}
# /* end look up table */



unknowns = set()  # create a "unique list"

def mycallback(match):
	myhash = (match.group(0)).upper()[3:-1]

	if myhash in mappings:
		replacement = mappings[myhash]
		if replacement[:2] == 'U+':
			return chr(int(replacement.lstrip("U+").zfill(8), 16))
		return replacement # assume an already prepared string here 
	
	print("Unknown DRCS hash: 0x", myhash, sep='', file=sys.stderr)
	unknowns.add(myhash)
	return '〓'

def main():
	
	ap = argparse.ArgumentParser(
		description=('Replaces known hashed ARIB DRCS symbols in subtitles files with human-readable equivalents.'),
		epilog='Report bugs, request features, or provide suggestions via https://github.com/TurtleWilly/arib-drcs-symbols/issues',
	)
	ap.add_argument('-V', '--version', action='version', help="show version number and exit", version='%(prog)s {}'.format(__version__), )
	ap.add_argument('input', type=str, help='input filename/path (*.ass, *.srt, etc.)')
	ap.add_argument('-o', '--output', metavar='FILENAME', type=str, help='output filename/path, if omitted it will be generated automatically')
	user_input = ap.parse_args()
	
	filename_in  = os.path.realpath(os.path.expanduser(user_input.input))
	
	if user_input.output:
		filename_out = os.path.realpath(os.path.expanduser(user_input.output))
	else:
		(root, extension) = os.path.splitext(filename_in)
		filename_out = root + '_fixed' + extension
	
	cached = re.compile('\[外:([0-9A-Fa-f]{32})\]')

	try:
		with open(filename_in, 'rt', encoding='utf8', newline=None) as fi, open(filename_out, 'xt', encoding='utf8', newline='\n') as fo:
			while True:
				line = fi.readline()
				if not line:  # end of file?
					break
				fo.write(cached.sub(mycallback, line.strip()) + '\n')
	except FileExistsError as e:
		print('Output file "{}" already exists.'.format(filename_out), file=sys.stderr)
	except OSError as e:
		print('Operation failed: {}'.format(e.strerror), file=sys.stderr)
	
	if unknowns:
		print("All unknown DRCS hashes: ", unknowns, file=sys.stderr)


if __name__ == "__main__":
	main()
