# Creating new offset database
### Auth-ticket 
1. Open Tribes of Midgard<br>
2. Open Cheat-engine<br>
3. In Cheat-engine select process Tribes of Midgard<br>
4. Text search for `1400000`<br>
5. Add results to address list<br>
6. Set the String length to 480(double-click the Type)<br>
7. Choose the value that has no weird symbols<br>
8. Remove the other value<br>
9. Generate pointermap for the value that is left and save it<br>
10. Close Tribes of Midgard<br>
11. Close Cheat-engine<br>
12. Repeat steps 1-8<br>
13. Pointer scan for the value that is left
14. Click Compare and select the pointermap you saved in step 9<br>
15. Select the file and the Address<br>
16. Hit ok<br>
17. Save the file as a name of your choice<br>
18. Wait for the scan to finish<br>
19. Click File in the top left corner<br>
20. Export to sqlite database
21. Name it `auth_offsets.db`<br>
22. Hit ok when it suggests you a name<br>
23. Hit Yes when asked if you want the table with indexes and keys<br>
24. Hit Yes when asked if you want resultid column filled<br>
25. Put `auth_offsets.db` into the program folder (where main.py is located)