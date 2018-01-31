# RepService
Database application for in-store registering of warranty and service/repair processes in general. It enables store staff to keep an organized log of the products left for repair by costumers, their route during the process and the communications made. Processes that require special attention, for instance because of a delay in delivery or while waiting for an answer from the costumer, are highlighted in the main list, in order to allow proper intervention by the staff team.


## Screenshots
1. Login window:

![login](https://user-images.githubusercontent.com/18650184/35652209-8da74808-06da-11e8-88ed-3e31d4b6e71c.png)

2. The overall aspect of the aplication (repairs list with message board, repair details and message/event details windows):

![service_msg_reparacoes](https://user-images.githubusercontent.com/18650184/27431379-4a942e82-5744-11e7-87cb-226f798a5bba.jpg)

3. Data insertion forms (new stock product repair, new shipment):

![service_rep_stock_e_remessas](https://user-images.githubusercontent.com/18650184/27431380-4abc89cc-5744-11e7-9c00-4ed3e39ddebd.jpg)

4. Data insertion forms (new costumer product repair, new contact):

![service_rep_cliente_e_contactos](https://user-images.githubusercontent.com/18650184/27431381-4ac27404-5744-11e7-804a-d4b5d58e7435.jpg)


## Dependencies
This application is being developed in Python 3.6 and tkinter, after and original idea by Márcio Araújo.

It requires, in its current version, the following external modules:

- Python MegaWidgets 2.0.1
- SQL Alchemy 1.1.5

Development and testing has been done only on Mac, however it should be pretty straightforward to make a few adaptations to make it run in Windows or Linux. The visual interface has been tweaked to match as much as possible Mac native applications, so at least the toolbars will certainly look a bit awkward in other plaforms. In older operating systems, some Unicode icons or emojis may not be correctly displayed. In Mac, it's highly recomendable to use ActiveTCL 8.5.18, as stated in Python language release documentation, in order to ensure compatibility and stability for tkinter in macOS.


## How to use
At this time, it is possible to configure some of the application's parameters (window dimensions and location, reducing animation for slower machines, database file location – only supporting a local sqlite database currently!), by changing the constants defined in the `service/global_setup.py` module.

Before running the application for the first time, you will need to initialize the database. During this early development stage, the module `service/db_local_main.py` can be executed directly, in order to generate a small sample database, populated with fake data.

To run the application, you just need to execute the module `service/service.py` with Python 3.6 or later. The default user is `npk` with the password `...` (yeah, no one in the entire world would ever come up with such a strong and safe password).
