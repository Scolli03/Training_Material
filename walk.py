import os
for root, dirs, files in os.walk("E:\Games DL"):
	for x in dirs:
		for file in os.listdir(os.path.join(root,x)):
			if file.endswith(".iso"):
                                try:
                                    os.remove(os.path.join(root,x,file))
                                except Exception as e:
                                    print(e)
