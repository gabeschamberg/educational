import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import signal

def sin_theta(t,f,a):
	return a*np.sin(t*2*np.pi*f)

def linear_theta(t,f,a):
	return t*f

def tri_theta(t,f,a):
	p = 1/f
	t = t % p
	if t < p/4:
		return t*(a/(p/4))
	elif p/4 <= t < 3*p/4:
		return 2*a - t*(a/(p/4)) 
	else:
		return -4*a + t*(a/(p/4))

def const_theta(t,f,a):
	return a

def animate_robot(alpha_type='linear', a1=5, f1=1/180.0, 
		  beta_type='triangle', a2=3, f2=1/45.0,
		  l1=100, l2=50, trace=False): 
	
	fig = plt.figure()
	if alpha_type == 'sin':
		alpha = sin_theta
	if alpha_type == 'linear':
		alpha = linear_theta
	if alpha_type == 'triangle':
		alpha = tri_theta
	if alpha_type == 'constant':
		alpha = const_theta
	
	if beta_type == 'sin':
		beta = sin_theta
	if beta_type == 'linear':
		beta = linear_theta
	if beta_type == 'triangle':
		beta = tri_theta
	if beta_type == 'constant':
		beta = const_theta

	ims = []
	xs = []
	ys = []
	for t in range(1000):
		theta1 = alpha(t,f1,a1)
		theta2 = beta(t,f2,a2) + theta1
		px1 = l1*np.cos(np.pi*theta1/180)
		py1 = l1*np.sin(np.pi*theta1/180)
		px2 = l2*np.cos(np.pi*theta2/180)
		py2 = l2*np.sin(np.pi*theta2/180)
		x1 = np.linspace(0,px1,abs(px1))
		y1 = (py1/px1)*x1
		x2 = np.linspace(0,px2,abs(px2))
		y2 = py1 + (py2/px2)*x2
		x2 = np.linspace(px1,px1+px2,abs(px2))
		xs.append(px1+px2)
		ys.append(py1+py2)
		if trace:
			im = plt.plot(xs,ys,'mo',x1,y1,'b',x2,y2,'r')
		else:
			im = plt.plot(x1,y1,'b',x2,y2,'r')
		l = l1 + l2
		plt.axis((-l,l,-l,l))
		ims.append(im)

	ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False)
	plt.show()
