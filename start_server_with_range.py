import http.server
import os
from http import HTTPStatus

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """支持HTTP范围请求的服务器处理器，解决视频无法快进问题"""
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        
        # 处理范围请求
        range_header = self.headers.get('Range')
        if range_header:
            # 解析Range请求（格式：Range: bytes=start-end）
            range_str = range_header.split('=')[-1]
            start_str, end_str = range_str.split('-')
            start = int(start_str) if start_str else 0
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)
            
            # 发送206 Partial Content响应（支持范围请求的状态码）
            self.send_response(HTTPStatus.PARTIAL_CONTENT)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
            self.send_header('Content-Length', str(end - start + 1))
            self.send_header('Last-Modified', self.date_time_string(os.path.getmtime(path)))
            self.end_headers()
            
            # 返回指定范围的文件数据
            f.seek(start)
            return f
        else:
            # 非范围请求，返回完整文件（兼容普通请求）
            return super().send_head()

if __name__ == '__main__':
    # 启动服务器，端口8000，支持范围请求
    host = '0.0.0.0'
    port = 8000
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, RangeHTTPRequestHandler)
    print(f"支持范围请求的服务器已启动")
    print(f"访问地址：http://localhost:{port}/index.html")
    print(f"按 Ctrl+C/关闭窗口 停止服务器")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("\n服务器已停止")