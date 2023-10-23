import pytermgui as ptg

with ptg.mouse_handler(["press", "hover"]) as mouse:
    while True:
      event = mouse(ptg.getch())
      print(type(event))
      print(event.action)
      print(event.position)

'pytermgui.ansi_interface.MouseEvent'
'pytermgui.ansi_interface.MouseAction.LEFT_CLICK'
(33, 55)


