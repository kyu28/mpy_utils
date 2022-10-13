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
  __path = ""
  __lines = []
  __ustack = [] # Stack to mark commands for undo
  __is_undo = False
  __edited = False

  def __init__(self, file):
    self.__methods = {'o': self.insert, 'd': self.delete, 'p': self.seek,
                      'w': self.write, 'u': self.undo}
    self.__path = file
    try:
      f = open(self.__path, "r")
      for i in f: self.__lines.append(i.rstrip())
      f.close()
    except FileNotFoundError: print("**New File**")
    
  def __parse(self, cmd):
    cmds = cmd.split(' ', 2)
    for i in cmds:
      if i == "":
        cmds.remove(i)
    if len(cmds) == 0: return False
    if cmds[0] in self.__methods:
      func = self.__methods[cmds[0]]
      func(cmds[1] if len(cmds) > 1 else None,
           cmds[2] if len(cmds) > 2 else None)
    elif cmds[0] == "q":
      if self.__edited:
        resp = input("Not saved, really quit? (y/N) ")
        if resp != 'y' and resp != 'Y': return False
      return True
    else:
      print("Invalid command")
    return False

  def __is_out_of_bound(self, lower, pos):
    if pos < lower or pos > len(self.__lines):
      print("Out of bound")
      return True
    return False

  def insert(self, pos, newline=None):
    pos = int(pos)
    if self.__is_out_of_bound(0, pos): return
    if not newline: newline = input("> ")
    self.__lines.insert(pos, newline.rstrip())
    if not self.__is_undo:
      self.__ustack.append(''.join(["d ", str(pos + 1)]))
    self.__edited = True

  def delete(self, pos, *placeholder):
    pos = int(pos) - 1
    if self.__is_out_of_bound(1, pos): return
    if not self.__is_undo:
      self.__ustack.append(''.join(["o ", str(pos), ' ', self.__lines[pos]]))
    print(self.__lines.pop(pos))
    self.__edited = True
    
  def seek(self, n=None, *placeholder):
    if n != None:
      try:
        n = int(n)
        if self.__is_out_of_bound(1, n): return
        self.__pointer = n
      except ValueError: pass
    if self.__pointer > len(self.__lines): self.__pointer = 1
    for i in self.__lines[self.__pointer - 1:self.__pointer + 4]:
      print(''.join([str(self.__pointer), ' ', i]))
      self.__pointer += 1

  def undo(self, *placeholder):
    if len(self.__ustack) == 0:
      print("Already at oldest change")
      return
    self.__is_undo = True
    self.__parse(self.__ustack.pop())
    self.__is_undo = False
    
  def write(self, path=None, *placeholder):
    if path != None: self.__path = path
    f = open(self.__path, 'w')
    for i in self.__lines: f.write(''.join([i, '\n']))
    f.close()
    self.__edited = False

  def interact(self):
    cmd = input(''.join(
      [self.__path, " (", str(len(self.__lines)), " lines): "]))
    return self.__parse(cmd)

def start(file):
  instance_sped = LineEditor(file)
  while not instance_sped.interact(): pass
  del instance_sped
