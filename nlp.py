import spacy
import re
from ip import run
from nltk import pos_tag
from images import image_data

nlp = None  # Placeholder for the spaCy NLP model

def load_models():
    global nlp
    nlp = spacy.load("en_core_web_sm")
    nlp_coref = spacy.load("en_coreference_web_trf")

    nlp_coref.replace_listeners("transformer", "coref", ["model.tok2vec"])
    nlp_coref.replace_listeners("transformer", "span_resolver", ["model.tok2vec"])

    nlp.add_pipe("coref", source=nlp_coref)
    nlp.add_pipe("span_resolver", source=nlp_coref)

def process_sentences_with_coref(sentences):
    # nlp = spacy.load("en_core_web_sm")
    # nlp_coref = spacy.load("en_coreference_web_trf")

    # nlp_coref.replace_listeners("transformer", "coref", ["model.tok2vec"])
    # nlp_coref.replace_listeners("transformer", "span_resolver", ["model.tok2vec"])

    # nlp.add_pipe("coref", source=nlp_coref)
    # nlp.add_pipe("span_resolver", source=nlp_coref)

    processed_docs = []  # To store processed docs to prevent garbage collection

    results = []
    for sentence in sentences:
        doc = nlp(sentence)
        processed_docs.append(doc)  # Store the processed Doc
        results.append({"sentence": sentence, "spans": doc.spans})

    return processed_docs, results


def replace_pronouns(updated_sentence, clusters_dict):
    for head, cluster in clusters_dict.items():
        for element in cluster:
            # Use regular expression to match whole words only
            pattern = r'\b' + re.escape(element) + r'\b'
            updated_sentence = re.sub(pattern, head, updated_sentence)
    return updated_sentence


def replace_nouns_with_image_paths(updated_sentence, image_paths_dict):
    for noun, image_path in image_paths_dict.items():
        updated_sentence = updated_sentence.replace(noun, image_path)
    return updated_sentence


def retrieve_image_paths(updated_sentence, image_data):
    image_paths_dict = {}  # Use a dictionary to store image paths with character as key

    # Process the updated sentence with spaCy
    doc = nlp(updated_sentence)

    # Extract nouns, adjectives, and verbs from the updated sentence
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    adjectives_verbs = [token.text for token in doc if token.pos_ in {"ADJ", "VERB"}]

    # Check if character or tags are mentioned in the updated sentence
    for item in image_data:
        character = item["character"]
        tags = item["tags"]
        image_path = item["image_path"]

        # Check if character matches a noun and at least one tag matches an adjective or verb in the sentence
        if character.lower() in [noun.lower() for noun in nouns] and any(
                tag.lower() in [adj_verb.lower() for adj_verb in adjectives_verbs] for tag in tags):
            if character not in image_paths_dict and tags:
                image_paths_dict[character] = image_path
            elif character in image_paths_dict and tags:
                # Replace the image path only if the existing path has empty tags
                if not image_data[next(idx for idx, val in enumerate(image_data) if val["character"] == character)][
                    "tags"]:
                    image_paths_dict[character] = image_path

        # If tags list is empty, only add the character to the image path dictionary
        if not tags and character.lower() in [noun.lower() for noun in nouns]:
            if character not in image_paths_dict:
                image_paths_dict[character] = image_path

    return image_paths_dict


def modify_sentence_with_image_paths(updated_sentence, image_paths_dict):
    # Extract image paths and prepositions from the updated sentence
    doc = nlp(updated_sentence)
    relevant_tokens = [token.text if token.text in image_paths_dict.values() or token.pos_ == "ADP" else "" for token in doc]
    
    # Remove empty strings and join the relevant tokens
    modified_sentence = " ".join(filter(None, relevant_tokens))
    
    return modified_sentence


def process_and_return_data(sentences):
    processed_docs, processed_sentences = process_sentences_with_coref(sentences)

    data = []  # Store modified sentences in the 'data' list

    # Process spans for each sentence using the processed_docs
    for doc, result in zip(processed_docs, processed_sentences):
        print("Original Sentence:", result["sentence"])
        print("Updated Sentence where pronoun is replaced by noun:")

        # Create a dictionary to store clusters
        clusters_dict = {}

        # Iterate over coref_head_clusters dynamically
        for i in range(1, 4):  # Adjust the range based on your requirement
            key = f'coref_head_clusters_{i}'
            clusters = result["spans"].get(key, [])
            if clusters:
                # Take the first element as key and append the text of the rest to its value
                key_str = str(clusters[0]) if clusters[0].text else str(clusters[0].root)
                value_str_list = [str(element.text) for element in clusters]
                clusters_dict[key_str.lower()] = value_str_list

        # Replace pronouns with corresponding nouns
        updated_sentence = result["sentence"]
        updated_sentence = replace_pronouns(updated_sentence, clusters_dict)

        print(updated_sentence)

        image_paths_dict = retrieve_image_paths(updated_sentence, image_data)

        # Replace nouns with corresponding image paths
        updated_sentence = replace_nouns_with_image_paths(updated_sentence, image_paths_dict)

        print("Updated Sentence with Image Paths:", updated_sentence)
        # print(updated_sentence)

        # Modify the sentence to keep only image paths and prepositions
        modified_sentence = modify_sentence_with_image_paths(updated_sentence, image_paths_dict)

        print("Modified Sentence with Image Paths:", modified_sentence)
        # print(modified_sentence)

        # Add the modified sentence to the 'data' list
        data.append(modified_sentence)

        print(clusters_dict)
        print()

    # Print the entire 'data' list
    print("The data which is input to the image positioning module: ")
    print(data)

    return data

# Example sentences
sentences = [
    "Once upon a time there was a lion in a jungle and he was sleeping under a tree",
    # "There came a rat and he was playing on sleeping lion",
    # "Suddenly the angry lion awake and he found a scared small rat",
    # "An angry lion grabbed the rat in a fist",
    # "The scared rat requested the lion to forgive him",
    # "The lion felt pity and left the rat",
    # "A rat ran away quickly",
    # "Another day the hunter threw a net on a lion and he was roaring for help",
    # "A rat came and cut the net and rescued the lion",
    # "Thereafter, the rat and lion became friends they lived happily in a jungle",
    # "lion on tree"
]

def clean_data(data_list):
    def remove_preposition(sentence):
        words = sentence.split()
        tagged_words = pos_tag(words)

        if tagged_words:
            first_word, last_word = tagged_words[0], tagged_words[-1]

            if first_word[1] == 'IN':  # Check if the first word is a preposition
                words = words[1:]

            if last_word[1] == 'IN':  # Check if the last word is a preposition
                words = words[:-1]

        return ' '.join(words)

    cleaned_list = [remove_preposition(sentence) for sentence in data_list]
    return cleaned_list


def extract_image_pairs(statement):
    words = statement.split()
    pairs = []
    current_pair = []

    for word in words:
        if word.endswith('.png'):
            if current_pair:  # If there's a current pair, add it to the pairs list
                pairs.append(tuple(current_pair))
                current_pair = [word]  # Start a new pair with the image file name
            else:
                current_pair.append(word)  # Start a new pair with the image file name
        elif word in ['on', 'under', 'above', 'in','up','down']:  # List of prepositions
            if len(current_pair) == 1:  # If there's only one image file name in the current pair
                current_pair.append(word)  # Add the preposition to the current pair
            else:
                if current_pair:  # If there's a current pair, add it to the pairs list
                    pairs.append(tuple(current_pair))
                current_pair = ["", word]  # Start a new pair with an empty string as the first element
        else:  # If it's not an image file name or a preposition
            if current_pair:  # If there's a current pair, add it to the pairs list
                pairs.append(tuple(current_pair))
                current_pair = []  # Reset current pair

    if current_pair:  # If there's still a current pair remaining after processing all words
        pairs.append(tuple(current_pair))

    return pairs


def merge_pairs(pairs):
    merged_pairs = []
    i = 0
    while i < len(pairs):
        if len(pairs[i]) == 2:  # If the tuple contains an image file name and a preposition
            if i + 1 < len(pairs):  # Ensure there's a next tuple
                merged_pairs.append(pairs[i] + pairs[i + 1])  # Merge the two tuples
                i += 1  # Increment i to skip the next tuple
            else:
                merged_pairs.append(pairs[i])  # Add the tuple as it is if it's the last one
        else:
            merged_pairs.append(pairs[i])  # Add the tuple as it is if it doesn't contain a preposition
        i += 1

    return merged_pairs


def insert_dummy_pairs(merged_pairs):
    dummy_pairs = []
    for pair in merged_pairs:
        if len(pair) == 1:  # If only one image file name is present in the pair
            dummy_pairs.append((pair[0], "on", "invisible.png"))  # Insert dummy tuple
        else:
            dummy_pairs.append(pair)  # Add the tuple as it is
    return dummy_pairs


def run_nlp(sentences):
    data=process_and_return_data(sentences)
    result=clean_data(data)
    pairs = extract_image_pairs(result[0])
    merged_pairs = merge_pairs(pairs)
    dummy=insert_dummy_pairs(merged_pairs)
    print(dummy)
    run(dummy)
    return "../static/images/composed_image.png"

# run_nlp(sentences)