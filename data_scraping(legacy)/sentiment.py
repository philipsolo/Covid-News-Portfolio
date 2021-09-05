from google.cloud import language_v1
from google.cloud.language_v1 import enums


def analyze_sentiment(text_content):
    cat_name = 'Not_available'
    cat_cat = 'Not_available'
    client = language_v1.LanguageServiceClient.from_service_account_json('key.json')
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    response_sent = client.analyze_sentiment(document, encoding_type=encoding_type)
    try:
        response_text_clasify = client.classify_text(document)
        for category in response_text_clasify.categories:
            cat_name = category.name
            cat_cat = category.confidence
    except:
        print('not long')

    sentiment_score = response_sent.document_sentiment.score
    sentiment_magnitude = response_sent.document_sentiment.magnitude

    return sentiment_score, sentiment_magnitude, cat_name, cat_cat


if __name__ == "__main__":
    print('runin')
