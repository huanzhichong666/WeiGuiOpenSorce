import time
import pigpio
import serial

class Sensors:
    @staticmethod
    def sensor_pressure_clean():
        """清零压力传感器传感器"""
        try:
            ser = serial.Serial(port="/dev/ttyAMA2", baudrate=38400)
            data = bytes.fromhex("20 06 00 02 00 01 EF 7B")
            ser.write(data)
            time.sleep(0.1)  # 等待初始化
            ser.close()
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def sensor_servor_clean():
        """清零舵机当前的角度"""
        try:
            ser = serial.Serial(port="/dev/ttyAMA2", baudrate=38400)
            data = bytes.fromhex("20 06 00 02 00 01 EF 7B")
            ser.write(data)
            time.sleep(0.1)  # 等待初始化
            ser.close()
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def sensor_distance_clean():
        """清零测距光电的数值"""
        try:
            ser = serial.Serial(port="/dev/ttyAMA2", baudrate=38400)
            data = bytes.fromhex("20 06 00 02 00 01 EF 7B")
            ser.write(data)
            time.sleep(0.1)  # 等待初始化
            ser.close()
        except Exception as e:
            print(f"Error: {e}")
class Leds:
    @staticmethod
    def enable_Led(pin, status):
        """使能或禁用LED灯"""
        try:
            pi = pigpio.pi()
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.write(pin, status)
            pi.stop()
        except Exception as e:
            print(f"Error: {e}")
class LinerMotor:
    @staticmethod
    def enable_motor(pin, status):
        """使能或禁用电机"""
        try:
            pi = pigpio.pi()
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.write(pin, status)
            pi.stop()
        except Exception as e:
            print(f"Error: {e}")



class MachineAct:


    @staticmethod
    def sensor_data_get(distance, speed):
        """获取传感器数据"""
        receive_times = int(distance * 10)  # 每0.1mm检测一次
        delay_time = 1 / (speed * 10)  # 每0.1mm所需时间
        result_list = []

        try:
            ser = serial.Serial(port="/dev/ttyAMA2", baudrate=38400)
            data = bytes.fromhex("20 03 00 00 00 02 C2 BA")

            for _ in range(receive_times):
                ser.write(data)
                time.sleep(delay_time)
                if ser.in_waiting:
                    raw_data = ser.read(ser.in_waiting).hex()
                    pressure = int(raw_data[6:10], 16) / 1000
                    result_list.append(pressure)
            ser.close()
        except Exception as e:
            print(f"Error: {e}")
        return result_list

    @staticmethod
    def linear_move_smooth(speed, times, distance):
        """平滑直线电机运动"""
        try:
            pi = pigpio.pi()
            if not pi.connected:
                raise Exception("Failed to connect to pigpio")

            dir_pin, pulse_pin = 20, 21
            pi.set_mode(dir_pin, pigpio.OUTPUT)
            pi.set_mode(pulse_pin, pigpio.OUTPUT)

            total_pulses = int(distance * 100)
            base_delay = int((1000000 / (100 * speed)) / 2)

            for _ in range(times):
                # 正向运动
                pi.write(dir_pin, 0)
                MachineAct._send_pulses(pi, pulse_pin, total_pulses, base_delay)
                time.sleep(0.1)

                # 反向运动
                pi.write(dir_pin, 1)
                MachineAct._send_pulses(pi, pulse_pin, total_pulses, base_delay)
                time.sleep(0.1)

            pi.stop()
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def _send_pulses(pi, pin, pulses, delay):
        """发送脉冲"""
        for _ in range(pulses):
            pi.write(pin, 1)
            time.sleep(delay / 1000000)
            pi.write(pin, 0)
            time.sleep(delay / 1000000)

    @staticmethod
    def servo_rotate(pin, angle):
        """控制舵机旋转到指定角度"""
        try:
            pi = pigpio.pi()
            pi.set_PWM_frequency(pin, 50)  # 设置频率为50Hz
            pulse_width = int((angle / 180.0) * 2000 + 500)  # 转换角度为脉宽
            pi.set_servo_pulsewidth(pin, pulse_width)
            time.sleep(0.5)  # 等待稳定
            pi.stop()
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def auto_get_distance():
        """自动获取移动距离"""
        try:
            pi = pigpio.pi()
            if not pi.connected:
                raise Exception("Failed to connect to pigpio")

            dir_pin, pulse_pin = 20, 21
            left_sensor, right_sensor = 19, 26
            pi.set_mode(dir_pin, pigpio.OUTPUT)
            pi.set_mode(pulse_pin, pigpio.OUTPUT)
            pi.set_mode(left_sensor, pigpio.INPUT)
            pi.set_mode(right_sensor, pigpio.INPUT)

            x1, x2 = 0, 0

            # 向右移动直到触发左侧光电传感器
            pi.write(dir_pin, 0)
            while pi.read(left_sensor):
                MachineAct._send_pulses(pi, pulse_pin, 100, 100)
                x1 += 1
                time.sleep(0.02)

            # 向左移动直到触发右侧光电传感器
            pi.write(dir_pin, 1)
            while pi.read(right_sensor):
                MachineAct._send_pulses(pi, pulse_pin, 100, 100)
                x2 += 1
                time.sleep(0.02)

            pi.stop()
            return x1, x2
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def enable_motor(pin, status):
        """使能或禁用电机"""
        try:
            pi = pigpio.pi()
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.write(pin, status)
            pi.stop()
        except Exception as e:
            print(f"Error: {e}")