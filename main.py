import streamlit as st
import serial
from crc import append_crc, verify_packet
import time
import csv
import os
from datetime import datetime

#Configuration

ser = serial.Serial(
    port ='COM7',         #port name
    baudrate = 115200,      #rate of communication or sending data (bits/sec)
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout = 1           #wait time for reading
)

timestamp2 = datetime.now().strftime("%Y-%m-%d__%H;%M;%S.%f")[:-3]
LOG_FILE = f"[csv] {timestamp2}.csv"
# LOG_FILE='s_log.csv'

if not os.path.exists(LOG_FILE):
    with open (LOG_FILE, 'w', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['Time Stamp'] + ['res_0[HEX]'] + ['res_1[HEX]'] + ['CH_con[HEX]'] + ['As_con [HEX]'] + ['CN_con[HEX]'] + ['Ph_con[HEX]'] + ['Sol_con[HEX]'] + ['Alarm'] + [' Status'])

try:
    st.set_page_config(page_title="AP4C communication", layout="wide")
    # st.write("### Server Connected")
    # st.text("Send Request to check data")
    if ser.is_open:
        st.write("### Server Connected")
        data_spot = st.empty()
        if 'i' not in st.session_state:
            st.session_state.i = 1
        @st.fragment(run_every=5)
        def func():
            st.write(st.session_state.i)
            st.session_state.i += 1
            with data_spot.container():
                # data = input("Enter hex values (space seperated): ").split()
                data=[161, 3, 00, 15, 0, 15]

                packet=append_crc(data) #adding crc to data

                bytes_sent=ser.write(packet)   #sending bytes packet and storing no. of bytes in bytes_sent
                # print(f"Sent: {packet}")
                # print(packet)
                # print(f"sent: {packet.hex(' ')}")
                # print(f"Total bytes written: {data}")

                time.sleep(0.5)  # even if data not received the program will not shut for this amount of time

                # Read a fixed-length binary response. readline()/rstrip() can
                # wait for or strip newline-valued bytes inside the protocol frame.
                line = ser.read(35)
                line_length = len(line)

                if line_length == 0:
                    st.info("Port Connected, No Data Received !")
                    return

                if line_length != 35:
                    st.warning(f"Incomplete response: received {line_length} of 35 bytes.")
                    ser.reset_input_buffer()
                    return

                crch, crcl, is_valid = verify_packet(line)
                if not is_valid:
                    st.error(f"Invalid response CRC (expected {crch:02X} {crcl:02X}).")
                    return

                if line[2] != 30:
                    st.error(f"Unexpected response byte count: {line[2]} (expected 30).")
                    return

                byte_array = line
                byte = byte_array[3:33]
                device_add = line[0]
                st.write(f"##### Device Address: {device_add} [{device_add:02x}]")

                var = ['res_0', 'res_1', 'CH_con', 'As_con', 'CN_con', 'Ph_con', 'Sol_con', 'Alarm', 'Status']
                # byte_array = line  # decimal array of 35 inputs
                # byte = byte_array[3:33]
                print(byte)
                # st.write(f"{byte}")
                col1, col2, col3, col4 = st.columns(4, gap='large', border=True)
                with col1:  ########33333333333333333################
                    j = 0
                    for i in range(0, 4, 2):
                        sum = (byte[i] * 256) + byte[i + 1]
                        # print(sum)
                        # print(f"{sum:016b}")
                        vari = var[j]

                        # print(f"{vari}: {sum}")
                        st.write(f"##### {vari} ")

                        st.info(f"{sum}")  # {sum: 04b}
                        j += 1

                with col2:  ########33333333333333333################
                    j = 2
                    for i in range(4, 13, 2):
                        sum = (byte[i] * 256) + byte[i + 1]
                        # print(sum)
                        # print(f"{sum:016b}")
                        vari = var[j]

                        # print(f"{var[j]}: {sum}")
                        st.write(f"##### {vari} ")

                        st.info(f"{sum}")  # {sum: 04b}

                        j += 1

                        # print("----")

                # for alarm and status
                with col3:
                    # Alarm
                    sum = (byte[14])
                    vari = var[7]
                    # print(f"Alarm: {sum}")
                    # print(f"{sum:04b}")
                    st.write(f"##### Alarm: {sum:08b}")
                    sixteen_bit = f"{sum:08b}"
                    lenS = len(sixteen_bit)
                    k = lenS
                    for val in sixteen_bit:
                        k -= 1
                        if val == '1':
                            # print(f'Alarm[{k}]: on')
                            # st.write(f'Alarm[{k+1}]: on')
                            st.success(f"Alarm[{k + 1}]: ON")
                        elif val != '1':
                            st.error(f"Alarm[{k + 1}]: OFF")
                    # print("----")
                with col4:
                    # Status
                    sum = (byte[15])
                    vari = var[8]
                    # print(f"Status: {sum}")
                    # print(f"{sum:04b}")
                    st.write(f"##### Status: {sum:08b}")
                    sixteen_bit = f"{sum:08b}"
                    lenS = len(sixteen_bit)
                    k = lenS
                    for val in sixteen_bit:
                        k -= 1
                        if val == '1':
                            # print(f'Status[{k}]: on')
                            # st.write(f'Status[{k+1}]: on')
                            st.success(f"Status[{k + 1}]: ON")
                        elif val != '1':
                            st.error(f"Status[{k + 1}]: OFF")

                st.write(f"#### Data received:")
                st.info(f"{line}")
                st.write(f"length of data: {line_length}")

                st.write(f"#### Usable Data: ")
                st.info(f"{byte}")

                st.write(f"##### Device Address: ")
                st.info(f"{line[0]}")
                st.write(f"##### Function Code: ")
                st.info(f"{line[1]}")
                st.write(f"##### No. Of Variable: ")
                st.info(f"{line[2]}")

    ################################## Logging this Data to log file###############################
                if not line:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}]Port Connected, but no data received.")
                else:
                    # 1 Capture Time Stamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    # print("done1-date and time values assigned")
                    # 2 Extract specific data (Adjust indices based on your device's protocol)
                    # Example: data1 is byte index 3, data2 is byte index 4,
                    # Match the big-endian 16-bit values shown in the dashboard.
                    data1 = f"{int.from_bytes(line[3:5], 'big'):04x}"
                    data2 = f"{int.from_bytes(line[5:7], 'big'):04x}"
                    data3 = f"{int.from_bytes(line[7:9], 'big'):04x}"
                    data4 = f"{int.from_bytes(line[9:11], 'big'):04x}"
                    data5 = f"{int.from_bytes(line[11:13], 'big'):04x}"
                    data6 = f"{int.from_bytes(line[13:15], 'big'):04x}"
                    data7 = f"{int.from_bytes(line[15:17], 'big'):04x}"
                    data8 = f"{line[17]:08b}"
                    data9 = f"{line[18]:08b}"
                    # print("done3-data9 value assigned")

                    # print("done4--converting 'line' to bytes then hex...")
                    full_payload = bytes(line).hex(' ')  #### converting 'line' to bytes then hex
                    # print("done4-converted")

                    data_csv = [data1, data2, data3, data4, data5, data6, data7, data8, data9]
                    # 3 Dump to csv
                    # print("logging data to csv...")
                    with open(LOG_FILE, 'a', newline='') as f:
                        writerr = csv.writer(f)  # ????
                        writerr.writerow([timestamp] + data_csv)
                        print(f"Data Logged: data1: {data1}, data2: {data2} at time: {timestamp}")

            # if ser.in_waiting > 0:
            #     line = ser.readline().decode('utf-8').rstrip()
            #     print("Received : " + line)
            # elif status=='/exit':
            #
            #     break

        func()
except Exception as e:
    print(f"Erorr: {e}")
