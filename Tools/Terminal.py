import pexpect
import threading
import time

class TerminalManager:
    def __init__(self):
        self.terminals = {}
        self.locks = {}
        self.buffers = {}
        
    def _read_output(self, terminal_id):
        terminal = self.terminals[terminal_id]
        while not terminal['closed']:
            try:
                data = terminal['process'].read_nonblocking(size=1024, timeout=0.1)
                self.buffers[terminal_id] += data
            except pexpect.TIMEOUT:
                continue
            except (pexpect.EOF, OSError):
                terminal['closed'] = True
                break
    
    def create_terminal(self, terminal_id):
        if terminal_id in self.terminals:
            return ValueError(f"终端 {terminal_id} 已存在")
        
        process = pexpect.spawn(
            '/bin/bash',
            encoding='utf-8',
            codec_errors='ignore',
            dimensions=(24, 80)
        )
        
        self.terminals[terminal_id] = {
            'process': process,
            'closed': False
        }
        self.buffers[terminal_id] = ""
        self.locks[terminal_id] = threading.Lock()
        
        thread = threading.Thread(
            target=self._read_output,
            args=(terminal_id,),
            daemon=True
        )
        thread.start()
        return f"终端 {terminal_id} 已创建 (PID: {process.pid})"
    
    def send_command(self, terminal_id, command):
        with self.locks[terminal_id]:
            terminal = self.terminals.get(terminal_id)
            if not terminal:
                raise ValueError(f"终端 {terminal_id} 不存在")
            if terminal['closed']:
                raise RuntimeError(f"终端 {terminal_id} 已关闭")
            
            self.buffers[terminal_id] = ""
            terminal['process'].sendline(command)
        return f"命令已发送到终端 {terminal_id}"
    
    def send_keys(self, terminal_id, keys):
        with self.locks[terminal_id]:
            terminal = self.terminals.get(terminal_id)
            if not terminal:
                raise ValueError(f"终端 {terminal_id} 不存在")
            if terminal['closed']:
                raise RuntimeError(f"终端 {terminal_id} 已关闭")
            
            self.buffers[terminal_id] = ""
            terminal['process'].send(keys)
        return f"按键已发送到终端 {terminal_id}"
    
    def get_output(self, terminal_id):
        terminal = self.terminals.get(terminal_id)
        if not terminal:
            raise ValueError(f"终端 {terminal_id} 不存在")
        return self.buffers[terminal_id]
    
    def close_terminal(self, terminal_id):
        with self.locks[terminal_id]:
            terminal = self.terminals.get(terminal_id)
            if not terminal:
                raise ValueError(f"终端 {terminal_id} 不存在")
            if terminal['closed']:
                return f"终端 {terminal_id} 已关闭"
            
            terminal['process'].close(force=True)
            terminal['closed'] = True
            del self.terminals[terminal_id]
            del self.buffers[terminal_id]
            del self.locks[terminal_id]
        return f"终端 {terminal_id} 已关闭"

def Send_Command(command, terminal_id, dir, manager: TerminalManager):
    if terminal_id not in manager.terminals:
        manager.create_terminal(terminal_id)
    manager.send_command(terminal_id, command)
    manager.send_command(terminal_id, "cd " + dir)
    time.sleep(2)
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def View_Terminal(terminal_id, manager: TerminalManager):
    if terminal_id not in manager.terminals:
        return ValueError(f"终端 {terminal_id} 不存在")
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def Send_Keys(keys, terminal_id, manager: TerminalManager, end_newline=False):
    if terminal_id not in manager.terminals:
        manager.create_terminal(terminal_id)
    manager.send_keys(terminal_id, keys)
    time.sleep(2)
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def Kill_Terminal(terminal_id, manager: TerminalManager):
    manager.close_terminal(terminal_id)
    return f"终端 {terminal_id} 已关闭"