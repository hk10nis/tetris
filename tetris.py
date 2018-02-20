import wx

class tetris:
    def __init__(self):
        tetris_app = wx.App()
        frame = wx.Frame(None,wx.ID_ANY,"TETRIS")
        frame.Show()
        tetris_app.MainLoop()

if __name__ == '__main__':
    tetris = tetris()
