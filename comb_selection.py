# Gọi thư việc pandas dưới tên pd cho việc xử lý data
import pandas as pd

# TestsCombinationsSelection class
class TCS:
   def __init__(self, input_path, output_path):
      # Khởi tạo object với 2 biến đường dẫn input và output
      self.input_path = input_path
      self.output_path = output_path

   def read_data(self):
      # Đọc dữ liệu từ file CSV
      data = pd.read_csv(self.input_path, header=None)

      # Đặt tiêu đề cột là dòng 2
      data.columns = data.iloc[1]

      self.data = data
      
      # Lấy test data từ dòng 8 trở đi
      self.test_columns = data.columns[12:]

   def grouped_test_data(self):

      # Lấy test data từ dòng 8 trở đi
      test_data = self.data.iloc[7:,:]

      # Chuyển data các kết quả test sang dạng số
      test_data[self.test_columns] = test_data[self.test_columns].apply(pd.to_numeric, errors='coerce')
      
      # Nhóm data theo serialnumber
      grouped_data = test_data.groupby("SerialNumber")
      grouped_data_list = [group for _, group in grouped_data]

      return grouped_data_list

   def create_delta_dict(self):
      # Tạo delta dict cho các tiêu chuẩn test được quy định
      delta_dict = {}
      for column in self.test_columns:
         if column.endswith("RSSI -60.0 QPSK [50/0]"):
            delta_dict[column] = 0.25
         elif column.endswith("Max Power QPSK [12/19]"):
            delta_dict[column] = 0.2
      return delta_dict


   # Hàm để chọn ra 10 tổ hợp test thoả mãn điều kiện trong mỗi nhóm
   def select_10test_combination(self, group):

      delta_dict = self.create_delta_dict()
      delta_columns = list(delta_dict.keys())

      # Dataframe mới chứa dữ liệu kết quả test
      _test_data = group[delta_columns]
      _10test_combinations = []

      # Sắp xếp dữ liệu theo từng tiêu chuẩn test
      sorted_test_data = _test_data.sort_values(by=delta_columns)

      # Số lượng kết quả test cần xem xét
      num_tests = len(sorted_test_data)

      # Duyệt qua từng kết quả test
      for i in range(num_tests - 9):
         # Lấy ra 10 tổ hợp test
         selected_samples = sorted_test_data.iloc[i:i+10]

         # Tính std deviation, nếu std nhỏ nhất >= 0.2 thì loại tổ hợp này
         stddev = selected_samples.std()
         if stddev.max() >= 0.2:
            continue

         # Tính các delta trong các spec cần tính, lưu lại dạng boolean
         deltas = {}
         for column in delta_columns:
            delta = selected_samples[column].max() - selected_samples[column].min()
            deltas[column] = delta < delta_dict[column]

         # Nếu tất cả đều thỏa điều kiện thì lưu tổ hợp này lại
         if all(deltas.values()):
            _10test_combinations.append({"sample_indexes": selected_samples.index, "stddev": stddev.max()})

      # Sắp xếp các tổ hợp theo std deviation nhỏ nhất đến lớn nhất
      sorted_combinations = sorted(_10test_combinations, key=lambda x: x["stddev"])

      # Lấy tổ hợp đầu tiên nếu có
      return sorted_combinations[0] if sorted_combinations else None

   def execute(self):
      self.read_data()
      grouped_data_list = self.grouped_test_data()

      # Giữ lại các dòng 1-7
      idx_to_keep = [0,1,2,3,4,5,6]

      # Tiến hành chọn tổ hợp và thêm các số dòng để giữ lại
      for _, group in enumerate(grouped_data_list, 1):
         comb = self.select_10test_combination(group)
         if comb is not None:
            sample_indexes = comb.get("sample_indexes", [])
            idx_to_keep.extend(sample_indexes)

      # Lọc data theo danh sách và xuất data
      selected_data = self.data.iloc[idx_to_keep]
      selected_data.to_csv(self.output_path, index=False, header=False)

if __name__ == '__main__':
   input_path = "C:/Users/dangk/Downloads/Rawdata.csv"
   output_path = "C:/Users/dangk/Downloads/Output1.csv"
   tcs = TCS(input_path, output_path)
   tcs.execute()