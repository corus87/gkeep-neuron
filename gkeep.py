# -*- coding: utf-8 -*-
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope import Utils
import gkeepapi

class Gkeep(NeuronModule):
    def __init__(self, **kwargs):
        super(Gkeep, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.login = kwargs.get('login', None)
        self.password = kwargs.get('password', None)
        self.items = kwargs.get('items', None)
        self.list = kwargs.get('list', None)
        self.split_word = kwargs.get('split_word', None)
        self.option = kwargs.get('option', None)
        self.pin_list = kwargs.get('pin_list', False)

        
        if self._is_parameters_ok():
            self.keep = gkeepapi.Keep()
            try:
                self.keep.login(self.login, self.password)
            except:
                raise MissingParameterException('[Gnote] Login failed, maybe you set a wrong password')

            if self.items:
                self.items = [self.items]
                if self.split_word:
                    self.items = [x for item in self.items for x in item.split(self.split_word)]
                self.items = [x.strip(' ') for x in self.items]
                
            if self.option == 'add':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To add a item, you need to specify the list parameter') 
                if self.items is None:
                    raise MissingParameterException('[Gnote] To add a item to your list, you need to specify the items parameter') 
                
                items = self.AddToList(self.list, self.items) 
                if items:
                    items = ', '.join(items)
                    self.say({'ItemsAdded': items,
                              'List': self.list})
                    
            if self.option == 'delete_list':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To delete a list, you need to specify the list parameter')
                deleted = self.DeleteList(self.list)
                self.say({'ListDeleted' if deleted else 'ListNotFound': self.list})
            
            if self.option == 'check_item':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To check a item, you need to specify the list parameter')
                if self.items is None:
                    raise MissingParameterException('[Gnote] To check a item, you need to specify the items parameter')
                items = self.CheckItem(self.list, self.items)            
                if items:
                    items = ', '.join(items)
                    self.say({'ItemsChecked': items,
                              'List': self.list})
                else:
                    self.say({'ListNotFound': self.list})

            if self.option == 'uncheck_item':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To uncheck a item, you need to specify the list parameter')
                if self.items is None:
                    raise MissingParameterException('[Gnote] To uncheck a item, you need to specify the items parameter')
                
                items = self.UnCheckItem(self.list, self.items)   
                if items:
                    items = ', '.join(items)
                    self.say({'ItemsUnchecked': items,
                              'List': self.list})
                else:
                    self.say({'ListNotFound': self.list})
            
            if self.option == 'delete_list_item':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To delete a item from your list, you need to specify the list parameter')
                if self.items is None:
                    raise MissingParameterException('[Gnote] To delete a item from your list, you need to specify the items parameter')
                    
                items = self.DeleteItem(self.list, self.items)
                if items:
                    items = ', '.join(items)
                    self.say({'ItemsDeleted': items,
                              'List': self.list})
                else:
                    self.say({'ListNotFound': self.list})
                    
            if self.option == 'get_all_lists':
                lists = self.ReadLists()
                lists = ', '.join(lists)
                self.say({'AllLists': lists})

            if self.option == 'get_list_items':
                if self.list is None:
                    raise MissingParameterException('[Gnote] To get the items from your list, you need to specify the list parameter')
                    
                items = self.ReadListItems(self.list)
                if items:
                    items = items.replace("☐ ", "").replace('\n',', ')
                    self.say({'ItemsInList': items,
                              'List': self.list})
                else:
                    self.say({'ListNotFound': self.list})
            
            if self.option == 'note':
                if self.note_title is None:
                    raise MissingParameterException('[Gnote] To get create a note, you need to specify the note_title parameter')
                if self.note is None:
                    raise MissingParameterException('[Gnote] To get create a note, you need to specify the note parameter')
                self.CreateNote(self.note_title, self.note)
        
   
    def AddToList(self, list, items):
        my_list = None
        processed_items = []
        for l in self.keep.all():
            if l.title.lower() == list.lower():
                my_list = l
                break
        if not my_list:
            Utils.print_info("List not available, create a new list")
            my_list = self.keep.createList(list)
        if self.pin_list:
            my_list.pinned = True
        else:
            my_list.pinned = False
        for item in items:
            for i in my_list.items:
                if i.text.lower() == item.lower():
                    i.checked = False
                    Utils.print_info("Item %s already in list" % str(i).replace("☐ ", ""))
                    break
            else:
                my_list.add(item, False)
                Utils.print_info("Add item %s to list" % item)
                processed_items.append(item)

        self.keep.sync()
        return processed_items
        
        
    def ReadListItems(self, list):
        for l in self.keep.all():
            if l.title == list:
                return l.text
                break
        else:
            Utils.print_info('[Gnote] List %s not found' % list)
            return False
            
    def ReadLists(self):
        all = []
        for l in self.keep.all():
            all.append(l.title)

        return all
    
    def DeleteItem(self, list, items):
        my_list = None
        processed_items = []
        for l in self.keep.all():
            if l.title.lower() == list.lower():
                my_list = l
                break
        if my_list:
            for item in items:
                for l in my_list.items:
                    if l.text.lower() == item.lower():
                        l.delete()
                        Utils.print_info('[Gnote] Item %s from %s deleted' % (item, list))
                        processed_items.append(item)
            self.keep.sync()
            return processed_items
        else:
            Utils.print_info('[Gnote] List %s not found' % list)
            return False

    def DeleteList(self, list):
        my_list = None
        for l in self.keep.all():
            if l.title.lower() == list.lower():
                my_list = l    
        if my_list:
            my_list.delete()
            self.keep.sync()
            Utils.print_info('[Gnote] List %s deleted' % list)
            return True
        else:
            Utils.print_info('[Gnote] List %s not found' % list)
            return False

    def CheckItem(self, list, items):
        my_list = None
        processed_items = []
        for l in self.keep.all():
            if l.title == list:
                my_list = l
                break
        if my_list:    
            for item in items:
                for i in my_list.items:
                    if i.text.lower() == item:
                        i.checked = True
                        Utils.print_info('[Gnote] Item %s on %s checked' % (item.replace("☐ ", ""), list))
                        processed_items.append(item)
                        break
 
            self.keep.sync()
            return processed_items
        else:
            Utils.print_info('[Gnote] List %s not found' % list)
            return False

    def UnCheckItem(self, list, items):
        my_list = None
        processed_items = []
        for l in self.keep.all():
            if l.title == list:
                my_list = l
                break
        if my_list:
            for item in items:
                for i in my_list.items:
                    if i.text.lower() == item:
                        i.checked = False
                        Utils.print_info('[Gnote] Item %s on %s unchecked' % (item.replace("☐ ", ""), list))
                        processed_items.append(item)
            
            self.keep.sync()
            return processed_items
        else:
            Utils.print_info('[Gnote] List %s not found' % list)
            return False

    def CreateNote(self, title, text):
        self.keep.createNote(title, text)
        self.keep.sync()

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """ 
        if self.option:
            options = ['add', 'delete_list', 'check_item', 'uncheck_item', 'delete_list_item', 'get_all_lists', 'get_list_items']
            if self.option not in options:
                raise MissingParameterException('[Gnote] %s is not a valid option' % self.option)
        else:
            raise MissingParameterException('[Gnote] You need to set a valid option')
        
        if self.login is None:
            raise MissingParameterException('[Gnote] You need to login with your email-address')
        if self.password is None:
            raise MissingParameterException('[Gnote] You need set your password')
            
        return True
