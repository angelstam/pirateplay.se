from ..rerequest import TemplateRequest

mtg_encode = [lambda v: { 'req_url': 'http://viastream.viasat.tv/PlayProduct/%s' % v['id'] },
			lambda v: { 'final_url': '%s swfVfy=1 swfUrl=http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player.swf' % v['final_url'].replace('/mp4:', '/ playpath=mp4:'),
						'quality': '%s kbps' % v['bitrate'] }]

tv3play = { 'title': 'TV3-play', 'url': 'http://tv3play.se/', 'startvars': { 'suffix-hint': 'flv' },
			'items': [TemplateRequest(
						re = r'^(http://)?(www\.)?tv[3681]0?play\.se/.*/(?P<id>\d+).*',
						encode_vars = mtg_encode[0]),
						
					TemplateRequest(
						re = r'<SamiFile>(?P<subtitles>[^<]*).*<Video>.*<BitRate>(?P<bitrate>\d+).*?<Url><!\[CDATA\[(?P<final_url>rtmp[^\]]+)',
						encode_vars = mtg_encode[1])] }
							
mtg_alt = { 'startvars': { 'suffix-hint': 'flv' },
			'items': [TemplateRequest(
						re = r'^(http://)?(www\.)?tv[3681]0?play\.se/.*/(?P<id>\d+).*',
						encode_vars = mtg_encode[0]),
						
					TemplateRequest(
						re = r'<SamiFile>(?P<subtitles>[^<]*).*<Video>.*<BitRate>(?P<bitrate>\d+).*?<Url><!\[CDATA\[(?P<req_url>http[^\]]+)'),
						
					TemplateRequest(
						re = r'<Url><!\[CDATA\[(?P<final_url>[^\]]+)',
						encode_vars = mtg_encode[1])] }

hls_init_req = TemplateRequest(
						re = r'(hls\+?)?(http://)?(www\.)?tv[3681]0?play\.se/.*/(?P<id>\d+).*',
						encode_vars = lambda v: { 'req_url': 'http://playapi.play.mtgx.tv/v3/videos/stream/%(id)s' % v } )
hls_main_m3u8_req = TemplateRequest(
						re = r'"hls":"(?P<req_url>(?P<base>http:.+/).+\.m3u8[^"]*)"',
						encode_vars = lambda v: { 'req_url': v['req_url'].replace('\\', ''), 'base': v['base'].replace('\\', '') } )

mtg_hls = { 'title': 'MTG TV*-play HLS #1',
			'items': [hls_init_req,
					hls_main_m3u8_req,
					TemplateRequest(
						re = r'BANDWIDTH=(?P<bitrate>\d+)[^\n]*\n(?P<url>[^\n]+)',
						encode_vars = lambda v: { 'final_url': '%(base)s%(url)s' % v,
													'quality': '%s kbps' % (str(int(v['bitrate'])/1000)),
													'suffix-hint': 'mp4' })] }

mtg_hls2 = { 'title': 'MTG TV*-play HLS #2',
			'items': [hls_init_req,
					hls_main_m3u8_req,
					TemplateRequest(
						re = r'BANDWIDTH=(?P<bitrate>\d+).*?RESOLUTION=(?P<resolution>\d+x\d+).*?\n(?P<final_url>[^\n]+)',
						encode_vars = lambda v: { #'final_url': '%(base)s%(url)s' % v,
													'quality': '%s kbps' % (str(int(v['bitrate'])/1000)),
													'suffix-hint': 'mp4' })] }

#Dummies: TV6-play and TV8-play is caught by tv3play and mtg_alt
tv6play = { 'title': 'TV6-play', 'url': 'http://tv6play.se/', 'feed_url': 'http://www.tv6play.se/rss/mostviewed' }
tv8play = { 'title': 'TV8-play', 'url': 'http://tv8play.se/', 'feed_url': 'http://www.tv8play.se/rss/recent' }

services = [tv3play, tv6play, tv8play, mtg_alt, mtg_hls, mtg_hls2]