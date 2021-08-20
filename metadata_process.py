import pandas as pd

# 文件路径
input_path = "./data/finger_data/"
output_file = "./data/tripartite_data_v5.csv"
course_question_path = "course_question.csv"
question_knowledge_path = "question_knowledge_is_main.csv"
question_knowledge_stdy_path = "knowledge_question_from_stdy.csv"
# v2 版本是全量数据running, 包含所有题型, 包含 作答数据question
# v5 版本是包含补充数据 running，包含所有题型
# v4 新增补充
knowledge_question_complement_path = "knowledge_question_complement.csv"

course_question = pd.read_csv(input_path + course_question_path)
question_knowledge = pd.read_csv(input_path + question_knowledge_path)
question_knowledge_stdy = pd.read_csv(input_path + question_knowledge_stdy_path)
knowledge_question_complement = pd.read_csv(input_path + knowledge_question_complement_path)

# 去重
question_knowledge = question_knowledge.drop_duplicates()
course_question = course_question.drop_duplicates()
question_knowledge_stdy = question_knowledge_stdy.drop_duplicates()
knowledge_question_complement = knowledge_question_complement.drop_duplicates()

# v2 版本是全量数据running, 包含所有题型, 包含 作答数据question
question_knowledge = question_knowledge[question_knowledge["is_main"] == 1]

#question_knowledge = question_knowledge[question_knowledge["is_main"] == 1]
#question_knowledge = question_knowledge[question_knowledge["is_multiple_choice"] == 1]

question_knowledge["kh_id"] = question_knowledge["kh_id"].apply(lambda x:"KnowledgePoint:" + x)
question_knowledge["question"] = question_knowledge["question"].apply(lambda x:"Question:" + x)

# 补充题
knowledge_question_complement = knowledge_question_complement[knowledge_question_complement["is_main"] == 1]
#knowledge_question_complement = knowledge_question_complement[knowledge_question_complement["is_multiple_choice"] == 1]
knowledge_question_complement["kh_id"] = knowledge_question_complement["kh_id"].apply(lambda x:"KnowledgePoint:" + x)
knowledge_question_complement["question_id"] = knowledge_question_complement["question_id"].apply(lambda x:"Question:" + x)


#course_question = course_question[course_question["is_multiple_choice"] == 1]
course_question["courseware_id"] = course_question["courseware_id"].apply(lambda x:"Courseware:" + x)
course_question["question_id"] = course_question["question_id"].apply(lambda x:"Question:" + x)

question_knowledge_stdy = question_knowledge_stdy[question_knowledge_stdy["is_main"] == 1]
#question_knowledge_stdy = question_knowledge_stdy[question_knowledge_stdy["is_multiple_choice"] == 1]
question_knowledge_stdy["knowledge_id"] = question_knowledge_stdy["knowledge_id"].apply(lambda  x:"KnowledgePoint:" + x)
# 虚拟 course - question
question_knowledge_stdy["virtual_course_id"] = question_knowledge_stdy["question_id"].apply(lambda x:"Courseware:VIRTUAL" + x )
question_knowledge_stdy["question_id"] = question_knowledge_stdy["question_id"].apply(lambda  x:"Question:" + x)


question_knowledge[["kh_id", "question"]].to_csv(output_file, sep="\t", header=None, index=False)
course_question[["question_id", "courseware_id"]].to_csv(output_file, sep="\t", header=None, mode="a", index=False)
question_knowledge_stdy[["knowledge_id", "question_id"]].to_csv(output_file, sep="\t", header=None, mode="a", index=False)
question_knowledge_stdy[["question_id", "virtual_course_id"]].to_csv(output_file, sep="\t", header=None, mode="a", index=False)
knowledge_question_complement[["kh_id", "question_id"]].to_csv(output_file, sep="\t", header=None, mode="a", index=False)

