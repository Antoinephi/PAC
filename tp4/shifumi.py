# -*- coding: utf8 -*-
from client import *
import random
import datetime

def legendre(a_, p):
	p_1 = (p-1 >> 1)
	a = pow(a_, p_1, p)
	# print(a)
	return a % p


def residu(g_x, g_y, reste, p):
	g_xy = (g_x * g_y) % p
	# print(g_x, '*', g_y)
	legendre_g_xy = legendre(g_xy, p)
	# print('reste :' , reste, '\np :', p)
	legendre_reste = legendre(reste, p)
	# print('g_xy : ', legendre_g_xy)
	# print('reste : ', legendre_reste)
	if legendre_g_xy == legendre_reste == 1 :
		return True
	return False

def XGCD(a, b):
	u = (1,0)
	v = (0,1)
	while b != 0:
		q, r = divmod(a, b)
		a = b
		b = r
		tmp = (u[0] - q*v[0], u[1] - q*v[1])
		u = v
		v = tmp
	return a, u[0], u[1] #a pgcd, u[0] inv de a dans b, [1] inv de b dans a

# server = Server('http://pac.bouillaguet.info/TP4/ElGamal-forgery')

# result = server.query('/PK/philippe')

# p = result['p']
# h = result['h']
# g = result['g']

p = 19848404999509110964365602426274530324743284491399023185644841089025026358503314008140990387939232266858286194051229983684070087088492279567082607586260577674446765854880429872622368224454854328019552695948374169860806152369899521010927700670424229419121248832504396071342903884011760667520976194398655765858397097631408058005607832883188133248466013937658864284530738705057898628322463655125320107000842474730753958970845475794745611403464278232319238222235960683673734377871390940341885110028332678982204220317559541619293793936253385402182496364821366527705501037470099068177204410696454701586675318613986237739233

h = 13586861152359393415982532128767931780166640390241450524375254596772683741163862757890225264712114598303462591498325010081567836009551471734310170924049598650765424358218730613337244690743076073785545480942498535209088422413433869813599439187747076253104923765553517211680818333083684580311254614272105334736582450683855737188023990754958418996073579028465727412519361388510829867898502962732064920793188647863311036156756865965302791419222700774314947806178548627586294972674724924880294723250452360763056677054097884327386274517891111736038875359367861715161069867369300264873414357918161510714209724766958563154097

g = 11862969420802482251006885030956813449668611894855139545133278118445568080308306997303004641348405413557042270568306042441345828241989488986192135631523048713450033930024136937417099924839819661731725931990435753711478038287091150893650006658502963236375930903949213812678687393190292378380870852839038619885456275594196367312751646564227225039981712285376525209169862990476134808494977473656841413315598250218441641791462183166577944804385723253128842833647401461254584283599508440123622294401885863384810882259125854555614953657423032359426752195022588233525384420293687286490716768966571381809770875652042152860106

# print(result)

#PIERRE : FEUILLE : CISEAUX
coups = [['PIERRE', 88275625857605],['FEUILLE', 19779480974019653], ['CISEAUX',18939445432636760]]



while True :
	server = Server('http://pac.bouillaguet.info/TP4/shifumi-deathmatch')

	#Demarre une partie

	result = server.query("/insert-coin/philippe")
	# print(result)

	result = server.query("/status/philippe")
	# print(result)

	try :
		while result['mine'] > 0 or result['yours'] > 0 :
			# print('while')
			# print(result['commitment'])
			result = server.query("/start/philippe")
			# print('apres query 1')
			# print(result)
			foobar = result['foobar']
			try :
				g_x = result['commitment']['PK']['h']
				g_y = result['commitment']['ciphertext'][0]
				p_ = result['commitment']['PK']['p']
				reste = result['commitment']['ciphertext'][1]
				first = 'first : server'
				if residu(g_x, g_y, reste, p_) == True :
					ind_coup = 0
				else :
					ind_coup = random.randrange(1,3)
				print("fail")
			except : 
				ind_coup = random.randrange(1,3)
				first = 'first : student'
			y = 42
			g_y = pow(g, y, p)
			h_y = pow(h, y, p)
			coup = coups[ind_coup][1]
			m = (coup * h_y) % p

			PK = {'p':p, 'g':g, 'h':h}
			ciphertext = []
			ciphertext.append(g_y)
			ciphertext.append(m)
			commitment = {'PK':PK, 'ciphertext':ciphertext}
			parameters = {'foobar':foobar, 'commitment':commitment}

			# print(parameters)
			result = server.query("/move", parameters)
			# print(result)
			# print('apres query 2')

			parameters = {'move':coups[ind_coup][0], 'k':y, 'barfoo':result['barfoo']}

			result = server.query("/result", parameters)
			# print('apres query 3')

			print(result['scores'], result['move'], coups[ind_coup][0], result['round-status'], first)
			# print(result)



			result = server.query("/status/philippe")
			# print(result)

	except Exception as e:
		print(e)
		# print("error")
		pass
	if len(str(result)) < 100 :	
		f = open('log', 'a+')
		out = str(datetime.datetime.now()) + ' ' +  str(result) + "\n"
		f.write(out)
		f.close()
