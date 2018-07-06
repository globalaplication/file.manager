# -*- coding: utf-8 -*-
#!/usr/bin/env python
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk
from config import Load
import functions

class Widget(Gtk.HBox):
    def __init__(beta, pictures, label):
        Gtk.Box.__init__(beta, spacing = 5, border_width = 3, halign = Gtk.Align.START)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename = pictures, 
        width=16, 
        height=16, 
        preserve_aspect_ratio = False)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        image.set_size_request(10, 10)
        beta.add(image)
        test = Gtk.Label(label)
        beta.add(test)

class MainWindow(Gtk.Window):
    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
    NUM_COLS) = range(5)
    IconWidth = 60
    CountFolder = 0
    CountText = 0
    CountHideFile = 0
    filedict = {}
    state = False

    def __init__(self):
        Gtk.Window.__init__(self, title = 'file.manager')
        functions.touchplaces()
        self.places = Load("/var/tmp/places")
        self.backgrounds = "/usr/share/backgrounds"
        self.Path = "/home/elementary"

        self.set_default_size(900, 800)
        self.set_border_width(10)
        
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "HeaderBar example"
        self.set_titlebar(self.hb)

        self.Geri = Gtk.Button()
        self.Geri.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.hb.add(self.Geri)
        self.Ileri = Gtk.Button()
        self.Ileri.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.hb.add(self.Ileri)

        self.GoEntry = Gtk.Entry()
        self.GoEntry.set_width_chars(20)
        self.GoEntry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,'gtk-apply')
        self.hb.pack_end(self.GoEntry)

        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-stop")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ToggleButton.add(image)
        self.hb.pack_end(self.ToggleButton)

        self.FormBox = Gtk.Box(spacing = 8, border_width = 0, halign = Gtk.Align.START)
        self.add(self.FormBox)

        self.box1 = Gtk.Box(halign = Gtk.Align.START)
        self.FormBox.pack_start(self.box1, 1, 1, 0)

        self.HeaderBar = Gtk.HeaderBar()
        self.HeaderBar.set_show_close_button(0)
        self.box1.pack_start(self.HeaderBar, 1, 1, 0)

        self.FlowBox = Gtk.FlowBox()
        self.FlowBox.set_valign(Gtk.Align.START)
        
        for picture in self.places.keyList():
            self.object = Widget("{}".format("./images.png"), "{}".format(picture) )
            self.FlowBox.add(self.object)

        self.HeaderBar.pack_start(self.FlowBox)

        self.box2 = Gtk.Box(spacing = 20, halign = Gtk.Align.START, valign = Gtk.Align.START)
 
        self.FormBox.pack_start(self.box2, 1, 1, 0)

        self.IconViewMenuBar = Gtk.MenuBar()
        self.IconViewInfoLabel = Gtk.MenuItem()
        self.IconViewMenuBar.append(self.IconViewInfoLabel)
        self.box2.add(self.IconViewMenuBar)

        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.box2.add(self.ScrolledWindow)

        self.IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        self.LoadIconView(self.IconViewStore)
        self.IconView = Gtk.IconView(model = self.IconViewStore)
        self.IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.IconView.set_text_column(self.FILENAME)
        self.IconView.set_pixbuf_column(self.FILEICON)
        self.IconView.set_item_width(self.IconWidth)
        self.IconView.set_margin(5)
        self.ScrolledWindow.add(self.IconView)

        self.ToggleButton.connect("toggled", self.HideFileShow, self.IconViewStore, '1')


    def HideFileShow(self, ToggleButton, IconViewStore, name):
        if self.ToggleButton.get_active():
            self.state = True
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
        else:
            self.state = False
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)

    def LoadIconView(self, IconViewStore, indextest = 0): 
        self.CountFolder, self.CountText, self.CountHideFile = 0, 0, 0
        self.GoEntry.set_text(self.Path)
        

        for enum, FileName in enumerate(os.listdir(self.Path),0):
            if FileName.startswith('.') is True and self.state is False:
                    indextest = indextest + 1
                    self.CountHideFile = self.CountHideFile + 1
                    continue
            self.filedict[enum-indextest] = {'file':self.Path+'/'+FileName, 
                    'isdir':os.path.isdir(os.path.join(self.Path, FileName))}
            if os.path.isdir(os.path.join(self.Path, FileName)) is True:
                self.CountFolder = self.CountFolder + 1
            else:
                self.CountText = self.CountText + 1
            self.IconViewStore.append(
            (os.path.join(self.Path, FileName), 
                FileName, 
                self.FileIcon(os.path.join(self.Path, FileName)
                    ),
                os.path.isdir(os.path.join(self.Path, FileName)
                    )
                )
            )
        if (self.CountFolder is 0 and self.CountText is 0):
            self.StatusBarInfo(str('Dizin boş'))
        else:
            info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
            self.StatusBarInfo(info) 


    def StatusBarInfo(self, String):
        StatusBarInfo = String
        self.IconViewInfoLabel.set_label(str(StatusBarInfo))
        #self.IconViewInfoLabel.select()
        #self.IconViewInfoLabel.activate()

    def FileIcon(self, path):
        fileicon = None
        giopath = Gio.file_new_for_path(path)
        query = giopath.query_info(Gio.FILE_ATTRIBUTE_STANDARD_ICON,
            Gio.FileQueryInfoFlags.NONE,
                    None)
        geticonnames = query.get_icon().get_names()
        icontheme = Gtk.IconTheme.get_default()
        for icon in geticonnames:
            try:
                fileicon = icontheme.load_icon(icon, 64, 0)
                break
            except GLib.GError:
                pass
        return fileicon
  

window = MainWindow()
window.connect('delete-event', Gtk.main_quit)
window.show_all()
Gtk.main()


