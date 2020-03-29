# Gkeep
Gkeep neuron for Kalliope

## Synopsis
Create and get your lists from google keep

## Installation
```bash
kalliope install --git-url https://github.com/corus87/gkeep-neuron
```

## Options

| Parameter   | Required | Choices                                 |
|-------------|----------|-----------------------------------------|
| login       | yes      | E-mail address                          |
| password    | yes      | Account password or APP password        |
| option      | yes      | add, delete_list, check_item, uncheck_item, delete_list_item, get_all_lists, get_list_items |
| items       | no       | A single or a list of items             |
| list        | no       | The name of your list. If the list not exist, it will create a new one with this name |
| split_word  | no       | A split word to create a lists of items e.g. Put on my shoppinglist the items milk and sugar and coffee |
| pin_list    | no       | True / False, if true your list get pinned |


## Return values

| Name           | Description                                  | Type   |
|----------------|----------------------------------------------|--------|
| ItemsAdded     | Returns the added items                      | list   |
| List           | Returns the name of your list                | string |
| ListDeleted    | Returns the name of the deleted list         | string |
| ItemsChecked   | Returns the checked items                    | list   |
| ListNotFound   | Returns the name of your list                | string |
| ItemsUnchecked | Returns the unchecked items                  | list   |
| ItemsDeleted   | Returns the name of the deleted items        | list   |
| AllLists       | Returns the names of your available lists    | list   |
| ItemsInList    | Returns the names of the items in your list  | list   |

## Notes
For this neuron I used an unofficial client for the Google Keep API. [Look here for more informations](https://github.com/kiwiz/gkeepapi/).

It is possible that you can't login with your default password, in this case try to setup an [APP password ](https://myaccount.google.com/apppasswords) for the neuron.

## Synapses example
```
  - name: "gkeep-add"
    signals:
      - order: "Add to {{ list }} the following {{ items }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"
          items: "{{ items }}"
          option: "add"
          split_word: "and"
          pin_list: True
          file_template: "templates/gkeep.j2"
          

  - name: "gkeep-delete-list"
    signals:
      - order: "delete list {{ list }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"
          option: "delete_list"
          file_template: "templates/gkeep.j2"

  - name: "gkeep-delete-list-item"
    signals:
      - order: "delete from {{ list }} following items {{ items }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"
          items: "{{ items }}"
          option: "delete_list_item"
          split_word: "and"
          file_template: "templates/gkeep.j2"

  - name: "gkeep-check-item"
    signals:
      - order: "check following {{ items }} in {{ list }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"
          items: "{{ items }}"      
          option: "check_item"
          split_word: "and"
          file_template: "templates/gkeep.j2"

  - name: "gkeep-uncheck-item"
    signals:
      - order: "uncheck following {{ items }} in {{ list }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"
          items: "{{ items }}"      
          option: "uncheck_item"
          split_word: "and"
          file_template: "templates/gkeep.j2"
  
  - name: "gkeep-get-all-list"
    signals:
      - order: "read all lists"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"     
          option: "get_all_lists"
          file_template: "templates/gkeep.j2"

  - name: "gkeep-get-list-items"
    signals:
      - order: "tell me what is on {{ list }}"
    neurons:
      - gkeep:
          login: "your@mail-address.com"
          password: "your_password"
          list: "{{ list }}"   
          option: "get_list_items"
          file_template: "templates/gkeep.j2"
          
```

## File template

```
{% if ItemsAdded %} 
    {{ ItemsAdded }} was added to your {{ List }}.
{% elif ListDeleted %} 
    {{ ListDeleted }} was deleted.
{% elif ItemsChecked %} 
    {{ ItemsChecked }} was checked on {{ List }}.
{% elif ItemsUnchecked %} 
    {{ ItemsUnchecked }} was unchecked on {{ List }}.
{% elif ItemsDeleted %} 
    {{ ItemsDeleted }} was deleted from {{ List }}.
{% elif AllLists %} 
    You got the following lists {{ AllLists }}
{% elif ItemsInList %} 
    Your lists {{ List }} contains the following items {{ ItemsInList }} 
{% elif ListNotFound %} 
    I could not find list {{ ListNotFound }}.
{% endif %}

```

## To-do
Create notes

