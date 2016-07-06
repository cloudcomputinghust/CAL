..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


      Convention for heading levels:
      =======  Heading 0 (reserved for the title in a document)
      -------  Heading 1
      ~~~~~~~  Heading 2
      +++++++  Heading 3
      '''''''  Heading 4
      (Avoid deeper levels because they do not render well.)


Testing CAL
===========

Testing framework
-----------------

Cần lưu ý, Test framework trong CAL chỉ là **Unit tests**, chứ không phải **Testing-Driven Developement** - TDD_, vì vậy sẽ chỉ viết test sau khi thiết kế và hoàn thành việc code chức năng.

.. _TDD: https://en.wikipedia.org/wiki/Test-driven_development

Unit Tests
~~~~~~~~~~

Quá trình phát triển
--------------------

Cấu trúc cây thư mục Unit Test 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cấu trúc cây thư mục Unit Test nên tương ứng với cấu trúc cây thư mục code cần test, và có thêm tiền tố 'test_' ví dụ: ::
    
    - target module: cal.wsgi
    
    - test.module: cal.tests.unit.test_wsgi

Cấu trúc thư mục `tests/`::

		├── base.py
		├── __init__.py
		├── fixtures.py
		└── unit
			├── conf_fixtures.py
			├── drivers
			├── __init__.py
			├── resources
			│   ├── compute
			│   │   └── __init__.py
			│   ├── file_fixtures.py
			│   ├── __init__.py
			│   ├── network
			│   │   └── __init__.py
			│   ├── storage
			│   │   └── __init__.py
			│   └── test_file_fixtures.py
			├── test_conf_fixtures.py
			├── test_connection.py
			└── test_wsgi.py

Trong đó:

- *base.py*: chứa các test utility và base TestCase, các lớp trong unit/ sẽ kết thừa lớp base TestCase này. 

- *fixtures.py*: chứa các Fixture cơ bản được sử dụng cho TestCase.

- *test_connection.py*: kiểm tra việc kết nối các cloud provider.(tùy chọn)

Cách viết testcase
------------------

**Lưu ý:**

1. *mock*: `mock` đơn giản là thay thế 1 đối tượng/lớp/phương thức bằng 1 đối tượng mock, và kiểm tra xem cách thức sử dụng, hoạt động của đối tượng đấy. Có thể định nghĩa mock object theo những cách sau - gọi là các **mock styles**:

- The nested context manager.

- Decorating the method or the class

- Mock/patcher objects	

Sau khi định nghĩa được các mock object, cần lưu ý đến hai attribute quan trọng sau:

- *side_effect*: attribute này sẽ giúp xác định behavior cho mock object. bằng việc raise những ngoại lệ Exception mong muốn hoặc hỗ trợ trả về nhiều hơn 1 kết quả `iterable` khi mock object được gọi.

- *return_value*: attribute định nghĩa kết quả được trả về khi mock object được gọi.

	Chi tiết tham khảo thêm `Slide`_ và `Docs`_

2. Phương thức *stub_out(old_func, new_func)* cho phép việc thay thế sử dụng 1 phương thức/hàm bằng 1 phương thức/hàm khác Lấy ví dụ `1 trường hợp sử dụng`_ trong test case của Openstack Nova:
	
	.. code-block:: python
	
		self.stub_out('os.chmod', lambda *a, **kw: None)

3. Về class skipIf() trong base.py, sẽ được sử dụng dưới dạng decorator khi muốn bỏ qua 1 phương thức test với điều kiện cho trước.

4. Cách viết 1 test case:

.. code-block:: python
	
	from cal.tests import base
	
	class TestSomeThing(base.TestCase):
		
		# Chuẩn bị môi trường cho việc test, 
		# thích hợp trong các trường hợp có 
		# những đoạn code lặp lại để chuẩn bị.
		def setUp(self):
			pass
		
		def test_method_one_case_one(self):
			pass
		
		def test_method_one_case_two(self):
			pass
			
		# Kết thúc việc test.
		def tearDown(self):
			pass	
			

5. KHÔNG SỬ DỤNG `MOX`_!

.. _MOX: https://pypi.python.org/pypi/mox
.. _Slide: https://docs.google.com/presentation/d/11N2sStyrKmRe6ubzabz5R-HWMHZDnfUEyULbtkdcSAA/edit#slide=id.g3bba25117_116
.. _Docs: https://docs.python.org/3/library/unittest.mock.html
.. _1 trường hợp sử dụng: https://github.com/openstack/nova/blob/master/nova/tests/unit/network/test_linux_net.py#L760

Chạy Unit Test
--------------

Dùng `tox`
~~~~~~~~~

CAL sử dụng `tox`_ để quản lý môi trường ảo nhằm phục vụ cho việc chạy test cases. Nó sử dụng `Testr`_ để quản lý việc chạy các test cases.

Tox xử lý việc tạo ra 1 loạt `virtualenvs`_.

Testr xử lý việc thực hiện song song một loạt các test cases cũng như tracking các long-running tests.

Để chạy unit tests::

    tox -e py27

Thông tin chi tiết có thể tham khảo tại trang wiki:
    
    https://wiki.openstack.org/wiki/Testr

.. _Testr: https://wiki.openstack.org/wiki/Testr
.. _tox: http://tox.readthedocs.org/en/latest/
.. _virtualenvs: https://pypi.python.org/pypi/virtualenv

Tài liệu tham khảo
------------------

1. `Note về unittest`_. 

.. _Note về unittest: https://gist.github.com/ntk148v/55154ea867555001c4aa47b970cac64b
