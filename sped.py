"""
A Simple ed

Usage:
  To start sped:
    import sped 
    sped.start("path/to/file")

  In sped:
    Insert a new line:
      o LINENUMBER [CONTENT]

    Delete a line:
      d LINENUMBER

    Seek 5 lines:
      p [LINENUMBER]

    Undo changes:
      u

    Save changes:
      w

    Exit
      q
"""
class LineEditor:
  __pointer = 1
  __filepath = ""
  __content = []
  __undostack = []
  __undoing = False
  __edited = False
  __methods = {'o': "insert", 'd': "delete", 'p': "seek",
               'w': "write", 'u': "undo"}

  def __init__(self, file):
    self.__filepath = file
    try:
      f = open(self.__filepath, "r")
      for i in f: self.__content.append(i.rstrip())
      f.close()
    except FileNotFoundError: print("**New File**")
    
  def __parse(self, cmd):
    cmds = cmd.split(' ', 2)
    for i in cmds:
      if i == "":
        cmds.remove(i)
    if len(cmds) == 0: return False
    if cmds[0] in self.__methods:
      exec_cmd = [ "self.", self.__methods[cmds[0]], "("]
      if len(cmds) > 1: exec_cmd += ['"', cmds[1], '"']
      if len(cmds) > 2: exec_cmd += [', "', cmds[2], '"']
      exec_cmd += ')'
      exec(''.join(exec_cmd))
    elif cmds[0] == "q":
      if self.__edited:
        resp = input("Not saved, really quit? (y/N) ")
        if resp != 'y' and resp != 'Y': return False
      return True
    else:
      print("Invalid command")
    return False

  def insert(self, pos, newline=None):
    pos = int(pos)
    if pos < 0 or pos > len(self.__content):
      print("Out of bound")
      return
    if not newline: newline = input("> ")
    self.__content.insert(pos, newline.rstrip())
    if self.__undoing:
      self.__undoing = False
    else:
      self.__undostack.append(''.join(["d ", str(pos + 1)]))
    self.__edited = True

  def delete(self, pos):
    pos = int(pos)
    if pos < 1 or pos > len(self.__content):
      print("Out of bound")
      return
    if self.__undoing:
      self.__undoing = False
    else:
      self.__undostack.append(''.join(
        ["o ", str(pos - 1), ' ', self.__content[pos - 1]]))
    print(self.__content.pop(pos - 1))
    self.__edited = True
    
  def seek(self, n=None):
    if n != None: self.__pointer = int(n)
    if self.__pointer > len(self.__content): self.__pointer = 1
    for i in self.__content[self.__pointer - 1:self.__pointer + 4]:
      print(''.join([str(self.__pointer), ' ', i]))
      self.__pointer += 1

  def undo(self):
    if len(self.__undostack) == 0:
      print("Already at oldest change")
      return
    self.__undoing = True
    self.__parse(self.__undostack.pop())
    
  def write(self, path=None):
    if path != None: self.__filepath = path
    f = open(self.__filepath, 'w')
    for i in self.__content: f.write(''.join([i, '\n']))
    f.close()
    self.__edited = False

  def interact(self):
    cmd = input(''.join(
      [self.__filepath, " (", str(len(self.__content)), " lines): "]))
    return self.__parse(cmd)

  def __del__(self):
    self.__filepath = ""
    self.__content = []
      
    
def start(file):
  instance_sped = LineEditor(file)
  while not instance_sped.interact(): pass
