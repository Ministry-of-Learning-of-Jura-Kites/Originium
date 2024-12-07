from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pathlib import Path

def get_from_path_or_none(data: dict, path: str | List[str]):
    if type(path) is not list:
        path = path.split(".")
    for property in path:
        if type(data) is not dict or property not in data:
            return None
        data = data[property]
    return data

@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    For multiple directories, use the following:
        FileIO().load(file_directories=['dir_1', 'dir_2'])

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    data_list = []
    for path in Path("Data 2018-2023/Project").glob("*/*"):
        try:
            print(path)
            data = FileIO().load(path, format='json')
            filtered_data = {}
            filtered_data['id'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'coredata', 'eid'])
            filtered_data['title'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'coredata', 'dc:title'])
            filtered_data["publication_name"] = get_from_path_or_none(data, ["abstracts-retrieval-response", "coredata", "prism:publicationName"],)
            filtered_data['abstract'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'item', 'bibrecord', 'head', 'abstracts'])
            filtered_data['publish_date'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'coredata', 'prism:coverDate'])
            filtered_data['cited_by_count'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'coredata', 'citedby-count'])
            filtered_data['reference_count'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'item', 'bibrecord', "tail", "bibliography", "@refcount"])
            filtered_data['classification_codes'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'subject-areas', 'subject-area'])
            filtered_data['affiliations'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'affiliation'])
            filtered_data['references'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'item', 'bibrecord', "tail", "bibliography", "reference"])
            filtered_data['keywords'] = get_from_path_or_none(data, ['abstracts-retrieval-response', 'authkeywords', 'author-keyword'])
            data_list.append(filtered_data)
        except Exception as e:
            print(f"Failed: {path}\nException: {repr(e)}")
    print("Reading files done.")
    merged_df = pd.DataFrame(data_list)

    return merged_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'