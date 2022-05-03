
# Smart & Secure Lock
[Visit Website]( https://sslock.herokuapp.com/)

In this current digital age, the security of highly sensitive places is very important. Newer and
newer technologies enable thieves to get through modern security systems easily. In order to
safeguard any place, a proper and secure locking system is needed. Implementation of the same
with technologies provided by the Internet of Everything along with the various wireless
technologies can prove effective in such scenarios.


## Steps to use
```
1. The proposed system uses ESP32 microcontroller for Wi-Fi connectivity, RC522 RFID
card reader with RFID card and tag, a 12V DC solenoid lock, and various LEDs to
display states. In the backend, a flask server handles various requests and responses
accordingly. Email service has been used to communicate with the user.
2. Initially the user needs to tap the card on the RFID reader. The system will check if the
user exists or not or else if the card is blocked or not.
3. If the card is blocked the user will receive an alert mail that some anonymous person is
using your card.
4. If the card is found correct, the user will get notified via a yellow LED that mail has been
sent. The user needs to open the mail and click on a suitable link to unlock it. There is a
threshold time of a minute for the user to enter the correct password. If the user fails to
enter the correct password within a minute then he needs to perform the above same steps
again.
5. If the entered password is correct, the solenoid lock gets unlocked and the white LED
will turn on, else the red LED will blink indicating that the entered password is wrong.
6. There is a facility provided to the user for blocking the card. When the user taps the card
on RFID and if the card is found correct, the user receives another link to block the card
with a threshold of 5 minutes.
7. Users can also visit  https://sslock.herokuapp.com/ to refer to the above steps.
```
    
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Screenshots

![](https://github.com/krupalvora/Smart-SecureLock/blob/main/images/sslock-4.png?raw=true)
![](https://github.com/krupalvora/Smart-SecureLock/blob/main/images/sslock-1.png?raw=true)
![](https://github.com/krupalvora/Smart-SecureLock/blob/main/images/sslock-2.png?raw=true)
![](https://github.com/krupalvora/Smart-SecureLock/blob/main/images/sslock-3.png?raw=true)


## Authors

- [@Tirth Thoria](https://github.com/acealtair13)
- [@Vivek Vadhiya](https://github.com/vivek992)
- [@Krupal Vora](https://github.com/krupalvora)

