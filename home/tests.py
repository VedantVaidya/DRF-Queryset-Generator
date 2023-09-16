# # model='''
# # class Author(models.Model):
# #     name=models.CharField(max_length=5)
# #     age=models.IntegerField()

# # class Book(models.Model):
# #     title=models.CharField(max_length=5)
# #     writer=models.ForeignKey(Author,on_delete=models.CASCADE)
# #     pages=models.IntegerField()

# # '''


# # a='''{
# #     title:{value},
# #     writer:{foreignvalue:{Author}},
# #     pages:{value}
# # }'''
# # a=a.replace(" ","")
# # a=a.replace("\n","")
# class Selectrelated:
#     selectrelated = ""

#     def expandselectrelaed(key, value, underscroll=True):
#         print(Selectrelated.selectrelated)
#         if underscroll:
#             Selectrelated.selectrelated = f"{key}"
#         else:
#             Selectrelated.selectrelated = (
#                 f"{Selectrelated.selectrelated},{Selectrelated.selectrelated}__{key}"
#             )
#         for i, j in value.items():
#             if type(j) is dict:
#                 Selectrelated.expandselectrelaed(i, j, False)


# start = "Book"
# models = {
#     "Author": ["name", "age"], 
#     "Book": ["title", {"writer": "Author"}, "pages"]}

# expected_output = {
#     "title": "value",
#     "writer": {"book": "value"},
#     "pages": "value",
# }

# for key, value in output.items():
#     if type(value) is dict:
#         Selectrelated.expandselectrelaed(key, value)


# if Selectrelated.selectrelated:
#     print(f"{start}.object.select_related({Selectrelated.selectrelated})")
# else:
#     print(f"{start}.objects.all()")


class QueryBuilder:
    def __init__(self, base_model):
        self.query = f"{base_model}.objects"

    def build_query(self, expected_output):
        select_related_fields = []

        for field, value in expected_output.items():
            if isinstance(value, dict):
                # It's a related field, use select_related
                related_model_name, related_value = list(value.items())[0]
                self.add_select_related(related_model_name)
                select_related_fields.append(related_model_name)
            else:
                # It's a normal field, filter by it
                self.filter(field, value)

        # Remove select_related calls for fields that should be filtered
        for field in select_related_fields:
            self.query = self.query.replace(f".select_related('{field}')", "")

        return self.query

    def add_select_related(self, related_model_name):
        self.query += f".select_related('{related_model_name}')"

    def filter(self, field_name, value):
        if "filter" not in self.query:
            self.query += ".filter("
        else:
            self.query += ", "
        self.query += f"{field_name}='{value}'"

    def get_query(self):
        if "filter" in self.query:
            self.query += ")"
        return self.query

# Updated Models and expected output
base_model = "Book"  # Specify the base model here
expected_output = {
    "title": "value",
    "writer": {"book": "value"},
    "pages": "value"
}

# Create QueryBuilder instance with the base model
query_builder = QueryBuilder(base_model)

# Generate the queryset string
query = query_builder.build_query(expected_output)

# Print the resulting queryset string
print(query)
