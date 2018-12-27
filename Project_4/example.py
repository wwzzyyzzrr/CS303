def innerL(i, oS):
    Ei = calcEk(oS, i)
	if ((oS.labelMat[i] * Ei < -oS.toler) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i] * Ei > oS.toler) and (oS.alphas[i] > 0)):
		j, Ej = selectJ(i, oS, Ei)      									 #第二个α选择的启发式方法
		alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy()  	 #进行深复制处理
		
		#根据公式[6]
		if (oS.labelMat[i] != oS.labelMat[j]):
			L = max(0, oS.alphas[j] - oS.alphas[i])
			H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
		else:
			L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
			H = min(oS.C, oS.alphas[j] + oS.alphas[i])
			
			
		if L == H: 
            print "L == H" 
            return 0
		
		#根据公式[5]
		eta = 2.0 *  oS.K[i, j] - oS.K[i, i] - oS.K[j, j]
		if eta >= 0:
            print "eta >= 0"
            return 0                             #??为什么eta>=0就可表示剪辑过？
		oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
		oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
		updatEk(oS, j)														#跟新误差缓存
		if (abs(oS.alphas[j] - alphaJold) < 0.00001):
			print "j not moving enough"; return 0
		oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * (alphaJold - oS.alphas[j])
		updatEk(oS, i)
		
		#根据公式[3]
		b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, i] - oS.labelMat[j] * (oS.labelMat[j] - alphaJold) * oS.K[i, j]
		b2 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, j] - oS.labelMat[j] * (oS.labelMat[j] - alphaJold) * oS.K[j, j]
	    
		#根据SMO中优化的部分选择b的公式
		if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): 
            oS.b = b1
		elif (o < oS.alphas[j]) and (oS.C > oS.alphas[j]): 
            oS.b = b2
		else: 
            oS.b = (b1 + b2) / 2.0
		return 1
	else: 
        return 0