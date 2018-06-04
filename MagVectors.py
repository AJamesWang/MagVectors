import wx
import wx.lib.mixins.inspection as wit
import wx.aui as aui

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

import numpy as np
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Line3DCollection

import scipy.constants as sp #consider swapping numpy out with scipy, although shouldn't be an issue here

import copy

class MainFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super(MainFrame, self).__init__(*args, **kw)
		self.Size = wx.Size(900, 500)


		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.hbox)

		self.makePlot()
		self.makeEngine()
		self.makeInput()

		self.makeMenuBar()

		self.CreateStatusBar()
		self.SetStatusText("Magnetism is cool!")

	def makePlot(self):
		self.plot=Plot(self)
		self.hbox.Add(self.plot, 1, wx.EXPAND)

	def makeEngine(self):
		self.engine=MathEngine(self.plot)

	def makeInput(self):
		self.input=Input(self, self.engine, self.plot)
		self.hbox.Add(self.input, 1, wx.EXPAND)

	def makeMenuBar(self):
		menuBar=wx.MenuBar()

		###   File Menu   ###
		fileMenu = wx.Menu()

		aboutItem = fileMenu.Append(-1, "&About", "Learn things!")
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

		creditsItem = fileMenu.Append(-1, "&Credits", "Hmmm, I wonder who made this?")
		self.Bind(wx.EVT_MENU, self.OnCredits, creditsItem)

		fileMenu.AppendSeparator()
		exitItem = fileMenu.Append(wx.ID_EXIT, "Exit")
		self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

		menuBar.Append(fileMenu, "&File")

		###   Help Menu   ###
		helpMenu = wx.Menu()

		lineItem = helpMenu.Append(-1, "&Creating Straight Wires", "Bzzt!")
		self.Bind(wx.EVT_MENU, self.OnLine, lineItem)

		curveItem = helpMenu.Append(-1, "&Creating Curved Wires", "Bzzt!")
		self.Bind(wx.EVT_MENU, self.OnCurve, curveItem)

		filterItem = helpMenu.Append(-1, "&Filtering Out Certain Intensities", "It's hard to explain")
		self.Bind(wx.EVT_MENU, self.OnFilter, curveItem)

		resItem = helpMenu.Append(-1, "&Change Graph Resolution")
		self.Bind(wx.EVT_MENU, self.OnRes, resItem)

		menuBar.Append(helpMenu, "&Help")

		###   Settings Menu   ###
		prefssMenu = wx.Menu()

		resolItem = prefssMenu.Append(-1, "Graph Resolution")
		self.Bind(wx.EVT_MENU, self.OnResol, resolItem)

		menuBar.Append(prefssMenu, "Preferences")

		self.SetMenuBar(menuBar)

	def OnAbout(self, event): wx.MessageBox("HUH THAT'S A LOT OF WORDS","About this thing", wx.OK|wx.ICON_INFORMATION)
	def OnCredits(self, event): pass
	def OnExit(self, event): self.Close(True)
	def OnLine(self, event): pass
	def OnCurve(self, event): pass
	def OnFilter(self, event): pass
	def OnRes(self, event): pass
	def OnResol(self, event): pass

class Plot(wx.Panel):
	def __init__(self, parent, *args, **kw):
		super(Plot, self).__init__(parent, *args, **kw)

		self.xRes=2
		self.yRes=2
		self.zRes=2

		self.figure = mpl.figure.Figure(figsize=(2,2))
		self.canvas = FigureCanvas(self, -1, self.figure)
		self.axes = self.figure.add_subplot(111, aspect='equal', projection='3d')
		# self.axes.set_anchor('C')
		self.axes.set_xlabel('x')
		self.axes.set_xlim(0,10)
		self.axes.set_ylabel('y')
		self.axes.set_ylim(0,10)
		self.axes.set_zlabel('z')
		self.axes.set_zlim(0,10)
		# self.axes.autoscale(False, tight=True)
		# self.axes.autoscale_view(tight=True)
		self.axes.view_init(elev=20)

		self.curFig = None


		# self.toolbar = NavigationToolbar(self.canvas)
		# self.toolbar.Realize()

		sizer = wx.BoxSizer()
		sizer.Add(self.canvas, 1, wx.EXPAND)
		# sizer.Add(self.toolbar, 1, wx.LEFT | wx.EXPAND)

		self.SetSizer(sizer)
		st = wx.StaticText(self, label="This will be a graph in the future")

		#self.refresh() moved to MathEngine constructor


	def filter(self): pass

	def drawLine(self, pos1, pos2, current):
		pos1 = np.array(pos1)
		pos2 = np.array(pos2)
		segment_length=1
		arrow_size=current/segment_length

		direction=pos2-pos1
		length=np.linalg.norm(direction)

		subCount=np.absolute(length/segment_length)
		curPos=pos2
		dPos=direction/subCount

		colour = 0*np.ones_like(curPos)

		for i in np.arange(np.floor(subCount)):
			curPos-=dPos
			self.axes.quiver(*curPos, *dPos, arrow_size, color=colour)

		dPos=curPos-pos1
		if not dPos.all==0:
			arrow_size=current/np.linalg.norm(dPos)
			self.axes.quiver(*pos1, *dPos, arrow_size, color=colour)

	def drawCurve(self, pos1, pos2, center, current):
		segment_length=.1
		arrow_freq=10
		arrow_size=.05*current/segment_length*arrow_freq

		r=np.abs(np.linalg.norm(pos1-center))
		r1=pos1-center
		r2=pos2-center
		perp=np.cross(r1, r2)
		theta=(2*np.pi + np.arccos(np.dot(r1, r2)))%(2*np.pi)

		dTheta=segment_length/r#segment_length/(2*np.pi*r)
		segmentCount=theta//dTheta
		curR=r2
		arrowCount=0

		# print("############")
		# print(r1)
		# print(r2)
		# print(perp)
		# print(theta)
		# print("##")
		# print(dTheta)
		# print(segmentCount)

		for i in np.arange(segmentCount):
			dR1 = curR-curR*np.cos(dTheta) # /r*r

			basis2=np.cross(curR, perp)
			basis2=basis2/np.linalg.norm(basis2)
			dR2=basis2*r*np.sin(dTheta)

			# print(str(i)+" ######")
			# print(np.linalg.norm(curR))
			# print(dR1-dR2)

			dR=dR1-dR2
			curR=curR-dR
			if arrowCount%arrow_freq==0:
				self.axes.quiver(*(curR+center), *dR, arrow_length_ratio=arrow_size)
			else:
				self.axes.quiver(*(curR+center), *dR, arrow_length_ratio=0)

			arrowCount+=1

		dR=curR-r1
		if not dR.all==0:
			# arrow_size=current/np.linalg.norm(dR)*(arrow_freq-arrowCount%arrow_freq)
			self.axes.quiver(*(r1+center), *dR, arrow_size)

	def drawVectors(self, vectors):
		z = vectors[0][:3]
		# u, v, w = np.zeros_like(vectors[0][3:])
		total = np.zeros_like(vectors[0])

		for vector in vectors:
			total[3:] = total[3:] + pow(10, 8)*vector[3:]
			# print(total[3:])

		total[:3] = vectors[0][:3]


		# print(x.shape, y.shape, z.shape, u.shape, v.shape, w.shape)
		# print(u, v, w)
		# total=[x, y, z, u, v, w]
		stepX=int(self.xRes/MathEngine.MAX_RES)
		stepY=int(self.yRes/MathEngine.MAX_RES)
		stepZ=int(self.zRes/MathEngine.MAX_RES)


		# xIndex = np.arange(0, len(total[0]), stepX)
		# yIndex = 
		# print(stepX, stepY, stepZ)

		colours = np.linalg.norm(total[3:], axis=0)
		print(colours.shape)

		# print("########################################")
		# print(total[3:] == vectors[0][3:])

		if not self.curFig == None:
			del(self.curFig)

		print(len(total))
		self.curFig = self.axes.quiver(*total[:, ::stepX, ::stepY, ::stepZ], length=1, color="green")#, colours[::stepX,::stepY,::stepZ]])# color=colours[:,::stepX, ::stepY, ::stepZ])
		# self.curFig.set_array(np.random.rand(np.prod(x.shape)))

	def refresh(self, lines, curves, vectors):
		self.axes.clear()
		self.axes.set_xlabel('x')
		self.axes.set_xlim(0,10)
		self.axes.set_ylabel('y')
		self.axes.set_ylim(0,10)
		self.axes.set_zlabel('z')
		self.axes.set_zlim(0,10)

		for line in lines:
			#@todo: does not check if current is 0
			print(line)
			self.drawLine(*line)
			print(line)

		for curve in curves:
			self.drawCurve(*curve)

		self.drawVectors(vectors)
		self.canvas.draw()

class MathEngine():
	CURVE = 'C'
	LINE = 'L'
	MAX_RES = 1

	def __init__(self, plot, *args, **kwargs):

		self.plot=plot
		self.lines=[]
		self.curves=[]
		self.vectors=[]
		self.changes=[]

		# self.update()

	def addLine(self, pos1, pos2, cur):
		self.changes.append(MathEngine.LINE)
		if cur<0:
			temp=pos2
			pos2=pos1
			pos1=temp
			cur=-cur
		self.lines.append([np.array(pos1), np.array(pos2), cur])
		print(self.plot)
		print("\"added\" line")

		self.update()

	def addCurve(self, pos1, pos2, center, cur):
		self.changes.append(MathEngine.CURVE)
		if cur<0:
			temp=pos2
			pos2=pos1
			pos1=temp
			cur=-cur
		self.curves.append([np.array(pos1), np.array(pos2), np.array(center), cur])
		print(self.curves)
		print("\"added\" curve")

		self.update()

	def undo(self):
		if self.changes[-1]==MathEngine.LINE:
			del(self.lines[-1])
		elif self.changes[-1]==MathEngine.CURVE:
			del(self.curves[-1])
		else:
			print("SOMETHING HAS GONE HORRIBLY WRONG IN MathEngine.undo(self)")
			raise Exception
		del(self.vectors[-1])
		self.update()

	def getLineField(self, a, b, current, X, Y, Z, U, V, W):
		for x in range(len(X)):
			for y in range(len(Y)):
				for z in range(len(Z)):
					index = (x, y, z)
					pos = (X[index], Y[index], Z[index])
					a_p = np.linalg.norm(pos - a)
					b_p = np.linalg.norm(pos - b)
					d = np.linalg.norm(np.cross(pos-a, pos-b))/np.linalg.norm(b-a)
					theta_0 = np.arcsin(d/a_p)
					theta_f = np.pi - np.arcsin(d/b_p)

					mag = sp.mu_0*current/(12*sp.pi) * (np.cos(theta_f)**3 - np.cos(theta_0)**3)

					direction = np.cross((a-pos), (b-pos))
					direction = direction/np.linalg.norm(direction)

					U[index], V[index], W[index] = np.array([U[index], V[index], W[index]]) + mag * direction

	def getCurveField(self, pos1, pos2, center, current, x, y, z, u, v, w):
		curveLines=[]

		segment_length=.1

		r=np.abs(np.linalg.norm(pos1-center))
		r1=pos1-center
		r2=pos2-center
		perp=np.cross(r1, r2)
		theta=(2*np.pi + np.arccos(np.dot(r1, r2)))%(2*np.pi)

		dTheta=segment_length/r#segment_length/(2*np.pi*r)
		segmentCount=theta//dTheta
		curR=r2


		#@todo: replace dR with point 2
		for i in np.arange(segmentCount):
			# Delta vector parallel to R1
			dR1 = curR-curR*np.cos(dTheta)

			# Delta vector perpendicular to R2 but still on the same plane as the circle
			basis2=np.cross(curR, perp)
			basis2=basis2/np.linalg.norm(basis2)
			dR2=basis2*r*np.sin(dTheta)

			# print(str(i)+" ######")
			# print(np.linalg.norm(curR))
			# print(dR1-dR2)

			dR=dR1-dR2
			nextR=curR-dR
			
			curveLines.append([curR, nextR, current])
			curR=nextR

		dR=curR-r1
		if not dR.all==0:
			# arrow_size=current/np.linalg.norm(dR)*(arrow_freq-arrowCount%arrow_freq)
			nextR=curR+dR
			curveLines.append([curR, nextR, current])

		for line in curveLines:
			self.getLineField(*line, x, y, z, u, v, w)

	def addVectors(self):
		X, Y, Z = np.meshgrid(np.arange(*self.plot.axes.get_xlim(), MathEngine.MAX_RES),
		                      np.arange(*self.plot.axes.get_ylim(), MathEngine.MAX_RES),
		                      np.arange(*self.plot.axes.get_zlim(), MathEngine.MAX_RES))
		U, V, W = np.zeros_like([X, Y, Z])

		vectors = np.array([X, Y, Z, U, V, W])

		if self.changes[-1]==MathEngine.LINE:
			self.getLineField(*self.lines[-1], *vectors)
			#do math
		elif self.changes[-1]==MathEngine.CURVE:
			self.getCurveField(*self.curves[-1], *vectors)
			# self.getCurveField(*self.curves[-1], u, v, w)
			#more math
		else:
			raise Exception("Well fuck")

		self.vectors.append(vectors)
		print("#####################################")
		print(len(self.vectors))

	def update(self, added=True):
		if added:
			self.addVectors()
		self.plot.refresh(self.lines, self.curves, self.vectors)

class Input(wx.Panel):
	def __init__(self, parent, engine, plot, *args, **kw):
		super(Input, self).__init__(parent, *args, **kw)
		self.engine=engine
		self.plot=plot
		self.vbox=wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.vbox)

		lines=self.makeLineInput()
		self.vbox.Add(lines)
		self.vbox.AddSpacer(20)
		curves=self.makeCurveInput()
		self.vbox.Add(curves)
		# self.makeSlideFilter()

	def makeLineInput(self):
		main = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		main.SetSizer(vbox)

		title = wx.StaticText(main, label="Add Straight Wire")
		vbox.Add(title)

		pnl = wx.Panel(main)
		grid = wx.GridSizer(3, 4, gap=wx.Size(5, 5))
		pnl.SetSizer(grid)

		line_1L = wx.StaticText(pnl, label="point 1 (x, y, z):")
		grid.Add(line_1L, wx.ALIGN_RIGHT)
		self.line_1x = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_1x)
		self.line_1y = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_1y)
		self.line_1z = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_1z)

		line_2L = wx.StaticText(pnl, label="point 2 (x, y, z):")
		grid.Add(line_2L, wx.ALIGN_RIGHT)
		self.line_2x = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_2x)
		self.line_2y = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_2y)
		self.line_2z = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_2z)

		line_cL = wx.StaticText(pnl, label="current (A):")
		grid.Add(line_cL, wx.ALIGN_RIGHT)
		self.line_c = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.line_c)

		line_b = wx.Button(pnl, -1, "Input Line")
		grid.Add(line_b)

		self.Bind(wx.EVT_BUTTON, self.addLine, line_b)

		vbox.Add(pnl)
		return main

	def addLine(self, event):
		# try:
			x1=float(self.line_1x.GetValue())
			y1=float(self.line_1y.GetValue())
			z1=float(self.line_1z.GetValue())

			x2=float(self.line_2x.GetValue())
			y2=float(self.line_2y.GetValue())
			z2=float(self.line_2z.GetValue())
			c=float(self.line_c.GetValue())

			self.line_1x.Clear()
			self.line_1y.Clear()
			self.line_1z.Clear()
			self.line_2x.Clear()
			self.line_2y.Clear()
			self.line_2z.Clear()
			self.line_c.Clear()

			self.engine.addLine([x1, y1, z1], [x2, y2, z2], c)
		# except:
		# 	wx.MessageBox("Sorry, something's not right", "You Fool", wx.OK)

	def makeCurveInput(self):
		main = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		main.SetSizer(vbox)

		title = wx.StaticText(main, label="Add Curved Wire")
		vbox.Add(title)

		pnl = wx.Panel(main)
		grid = wx.GridSizer(4, 4, gap=wx.Size(5, 5))
		pnl.SetSizer(grid)

		curve_1L = wx.StaticText(pnl, label="point 1 (x, y, z):")
		grid.Add(curve_1L, wx.ALIGN_RIGHT)
		self.curve_1x = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_1x)
		self.curve_1y = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_1y)
		self.curve_1z = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_1z)

		curve_2L = wx.StaticText(pnl, label="point 2 (x, y, z):")
		grid.Add(curve_2L, wx.ALIGN_RIGHT)
		self.curve_2x = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_2x)
		self.curve_2y = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_2y)
		self.curve_2z = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_2z)

		curve_3L = wx.StaticText(pnl, label="center (x, y, z):")
		grid.Add(curve_3L, wx.ALIGN_RIGHT)
		self.curve_3x = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_3x)
		self.curve_3y = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_3y)
		self.curve_3z = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_3z)

		curve_cL = wx.StaticText(pnl, label="current (A):")
		grid.Add(curve_cL, wx.ALIGN_RIGHT)
		self.curve_c = wx.TextCtrl(pnl, size=wx.Size(50, -1))
		grid.Add(self.curve_c)

		curve_b = wx.Button(pnl, -1, "Input curve")
		grid.Add(curve_b)

		self.Bind(wx.EVT_BUTTON, self.addCurve, curve_b)

		vbox.Add(pnl)
		return main

	def addCurve(self, event):
		try:
			x1 = float(self.curve_1x.GetValue())
			y1 = float(self.curve_1y.GetValue())
			z1 = float(self.curve_1z.GetValue())

			x2 = float(self.curve_2x.GetValue())
			y2 = float(self.curve_2y.GetValue())
			z2 = float(self.curve_2z.GetValue())

			x3 = float(self.curve_3x.GetValue())
			y3 = float(self.curve_3y.GetValue())
			z3 = float(self.curve_3z.GetValue())

			c = float(self.curve_c.GetValue())

			# if (np.linalg.norm(np.array([x1-x3, y1-y3, z1-z3]))
			# 	- np.linalg.norm(np.array([x2-x3, y2-y3, z2-z3]))) > 10**-5:
			# 	# print((np.linalg.norm(np.array([x1-x3, y1-y3, z1-z3]))
			# 	# - np.linalg.norm(np.array([x2-x3, y2-y3, z3-z3]))))
			# 	print("here")
			# 	raise ValueError()

			self.engine.addCurve([x1, y1, z1], [x2, y2, z2], [x3, y3, z3], c)

			self.curve_1x.Clear()
			self.curve_1y.Clear()
			self.curve_1z.Clear()
			self.curve_2x.Clear()
			self.curve_2y.Clear()
			self.curve_2z.Clear()
			self.curve_3x.Clear()
			self.curve_3y.Clear()
			self.curve_3z.Clear()
			self.curve_c.Clear()
		except ValueError:
			self.engine.undo()
			wx.MessageBox("Sorry, that doesn't create a circle", "Math is hard, I understand", wx.OK)
		# except:
		# 	wx.MessageBox("Sorry, something's not right", "You Fool", wx.OK)

if __name__=='__main__':
	app = wit.InspectableApp()
	frame = MainFrame(None, title="Electromagnetic Fields")
	frame.Show()
	app.MainLoop()