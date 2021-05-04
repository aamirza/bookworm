# Bookworm – a reading tracker

Bookworm is a command-line application that allows you to set a book reading goal and keep track of your progress
towards completing that goal. This is done by giving recommendations on how much you should read to stay on track
towards goal completion.

### Example

```
user$ bookworm

You are 16 days ahead on your goal to read 35 books by January 1, 2022

You have completed 10 books so far.

Fulfill one of these recommendations to stay on track:

2. Data Structures & Algorithms in Python – You need to read from page 171 to page 208 today.
3. The Great Game – You need to read from 7:07:37 to 8:26:46 today.
6. A Tale of Two Cities – You need to read from 69% to 76% today.
8. Invisible Women: Data Bias In A World Designed For Men – You need to read from 4:53:59 to 5:37:49 today.

`````

# Table of Contents

* [Bookworm – a reading tracker](#bookworm--a-reading-tracker)
  * [Example](#example)
* [Table of Contents](#table-of-contents)
* [Installation &amp; Initial Setup](#installation--initial-setup)
    * [Setting a goal](#setting-a-goal)
* [Guide](#guide)
    * [Adding your first book](#adding-your-first-book)
        * [Adding Audiobooks with length measured in time, and (e-)Books measured in per cent complete](#adding-audiobooks-with-length-measured-in-time-and-e-books-measured-in-per-cent-complete)
    * [Updating a book](#updating-a-book)
    * [Dropping a book](#dropping-a-book)
    * [Getting recommendations](#getting-recommendations)
* [Commands](#commands)
    * [Goal commands](#goal-commands)
    * [Book commands](#book-commands)
    * [Recommendation commands](#recommendation-commands)
* [Licence](#licence)

# Installation & Initial Setup

Bookworm is available through PyPi and can be installed with ```pip```

```$ pip install bkwrm```

## Setting a goal

Once successfully installed, the program can be invoked by typing `````bookworm````` into the command line.

```$ bookworm```

If you do not have a goal set, this command will walk you through the goal set-up process.

```
$ bookworm
How many books would you like to read? >>> 30
By when do you want to achieve this goal? [YYYY-MM-DD] >>> 2022-01-01
```

If you already have a goal set, the ```bookworm``` command will give you recommendations to help you stay on track.

# Guide

## Adding your first book

You can add a book by invoking the ```add_book``` or ```ab```command for short.

Three additional arguments are required: **title**, **pages read**, and **total pages**.

```$ bookworm ab "The Future Is Faster Than You Think" 12 269```

Note: The title must be placed inside quotation marks if longer than one word. Total pages must be greater than pages
read.

### Adding Audiobooks with length measured in time, and (e-)Books measured in per cent complete

Not all books have pages and page numbers. Bookworm allows you to add books with lengths measured in hours (HH:MM:SS),
and per cent complete (out of 100).

To change the way book length is measured, use the ```-f``` or ```-FORMAT``` tag.

There are three formats to choose from:

* ```book``` or ```b``` (the default), for books measured in pages.
* ```audiobook``` or ```ab```, for books measured in time (HH:MM:SS)
* ```ebook``` or ```eb```, for books measured in per centage.

**Example 1 (Audiobooks)**:

```$ bookworm ab -f ab "Deng Xiaoping and the Transformation of China" 2:13:16 32:37:49```

**Example 2 (E-Books)**:

```$ bookworm ab -f eb "The Skeptics Guide to the Universe" 78 100```

(note: no per centage other than 100 can be selected for e-books)

WARNING: Once you have selected a format, there is no way to change it later.

## Updating a book

When you call ```bookworm``` you will be shown reading recommendations

```
user$ bookworm

You are 16 days ahead on your goal to read 35 books by January 1, 2022

You have completed 10 books so far.

Fulfill one of these recommendations to stay on track:

2. Data Structures & Algorithms in Python – You need to read from page 171 to page 208 today.
3. The Great Game – You need to read from 7:07:37 to 8:26:46 today.
6. A Tale of Two Cities – You need to read from 69% to 76% today.
8. Invisible Women: Data Bias In A World Designed For Men – You need to read from 4:53:59 to 5:37:49 today.

`````

In the example above, the numbers 2, 3, 6, and 8 are known as the **IDs** of the book. As opposed to writing the title
every time you want to update your reading progress, you will use this ID.

To update your reading progress, add the command ```update_book``` or ```up```or ```ub```, choose the ID of the book you
want to update, and add in a page number.

In the example above, to update A Tale of Two Cities (ID #6) so that it is 81% read, you would do the following

```$ bookworm up 6 81```

This will update your reading progress and give you new recommendations. To update Audiobooks, add in your progress in
HH:MM:SS.

```$ bookworm up 8 6:02:04```

## Dropping a book

For the time being, once you start a book you are obligated to complete it! The ability to drop books is planned for
future releases.

## Getting recommendations

Typing ```bookworm``` will get you the reading recommendations you need to stay on track.

```
user$ bookworm

You are 16 days ahead on your goal to read 35 books by January 1, 2022

You have completed 10 books so far.

Fulfill one of these recommendations to stay on track:

2. Data Structures & Algorithms in Python – You need to read from page 171 to page 208 today.
3. The Great Game – You need to read from 7:07:37 to 8:26:46 today.
6. A Tale of Two Cities – You need to read from 69% to 76% today.
8. Invisible Women: Data Bias In A World Designed For Men – You need to read from 4:53:59 to 5:37:49 today.

`````

If you are **ahead** on your goal ("You are 16 days ahead on your goal"), recommendations will be made so that if you
followed through on them, you will be an additional day ahead on your goal. In this case, 17 days ahead.

In the case you are **behind** on your goal, recommendations will be made so that if you followed throgh on them, you
would have caught up to where you should be: neither behind or ahead, but on track.

If you are *very* behind on your goal, but want a small achievable goal you can reach, typing in ```bookworm next_day```
or ```bookworm nd``` will give you recommendations so that you are one less day behind on your goal.

```
user$ bookworm nd

You are -40 days behind on your goal to read 30 books by January 1, 2022

You have completed 10 books so far.

7. India After Gandhi – You need to read from page 20 to page 31 today.
12. Welcome to the Universe: An Astrophysical Tour – You need to read from page 47 to page 51 today.
```

In this case, following through on the above "next day" recommendations will drop the days behind counter from -40 to
-39.

# Commands

The following is a full list of commands and their options. This list can be accessed with ```bookworm -h``` and a list
of arguments can be viewed with ```bookworm [command] -h```

## Goal commands

* ```add_goal``` - add a new book reading goal (you may only have one at a time).
* ```ag``` - shorthand for add_goal
* ```update_goal``` - make changes to the goal in progress (book goal, target date).
* ``` ug``` - shorthand for update_goal.

## Book commands

* ```add_book``` - add a book to your self.
* ```ab``` - shorthand for add_book.
* ```update_book``` - update the properties of a book on your shelf.
* ```up``` - shorthand for update_book.
* ``` ub``` - shorthand for update_book.
* ```drop_book``` - drop or delete a book from the shelf. (unimplemented)
* ```db``` - shorthand for drop_book
* ```dp``` - shorthand for drop_book

## Recommendation commands

* ```next_day``` - get recommendations so that you are one day closer to completing your goal if you follow through.
* ```nd``` - shorthand for next_day.
* ```all``` - show list of recommendations as well as list of books you have already completed (hidden by default).

# Licence

The source code for this app is licensed under the MIT licence, which you can find in the LICENCE file.
