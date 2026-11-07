import os

def generate_academic_pdf(filepath):
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    pages = [
        # Page 1
        [
            'DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING',
            'COURSE: ARTIFICIAL INTELLIGENCE & GENERATIVE AI',
            'UNIT 3: NATURAL LANGUAGE PROCESSING FOUNDATIONS',
            '',
            '1. Introduction to Natural Language Processing (NLP)',
            'Natural Language Processing is a subfield of computer science and artificial',
            'intelligence concerned with interactions between computers and human language.',
            'Key tasks include tokenization, part-of-speech tagging, and syntactic parsing.',
            'Statistical language models estimate the probability of word sequences.',
            'Traditional n-gram models suffered from sparsity and inability to capture long context.'
        ],
        # Page 2
        [
            'UNIT 3: DEEP LEARNING FOR LANGUAGE',
            '',
            '2. Recurrent Neural Networks (RNN) and LSTMs',
            'Recurrent Neural Networks introduced recurrent feedback loops allowing sequence memory.',
            'Vanishing and exploding gradient issues made long-range dependency capture difficult.',
            'Long Short-Term Memory (LSTM) networks addressed this with input, forget, and output gates.',
            'Gated Recurrent Units (GRU) simplified the architecture with reset and update gates.',
            'Sequence-to-sequence encoder-decoder frameworks laid the groundwork for modern models.'
        ],
        # Page 3
        [
            'UNIT 3: THE TRANSFORMER REVOLUTION',
            '',
            '3. Attention Mechanisms and Self-Attention',
            'Vaswani et al. (2017) introduced Attention Is All You Need, eliminating recurrence.',
            'Self-attention allows the model to weigh the importance of all tokens in parallel.',
            'Multi-head attention projects queries, keys, and values into multiple representation subspaces.',
            'Positional encodings provide the network with sequence order awareness.',
            'Pretrained models like BERT, GPT, and Gemini achieved state-of-the-art results across tasks.'
        ],
        # Page 4
        [
            'UNIT 3: VECTOR EMBEDDINGS & SEMANTIC SEARCH',
            '',
            '4. Dense Representations and Vector Databases',
            'Words and documents are mapped into continuous dense high-dimensional vector spaces.',
            'Cosine similarity measures the semantic distance between queries and stored documents.',
            'Approximate Nearest Neighbor (ANN) indexing enables fast search over millions of items.',
            'FAISS (Facebook AI Similarity Search) is an efficient library for dense vector indexing.',
            'Vector databases serve as external memory for Large Language Models.'
        ],
        # Page 5
        [
            'UNIT 3: RETRIEVAL-AUGMENTED GENERATION (RAG)',
            '',
            '5. Retrieval-Augmented Generation in Educational Systems',
            '',
            'Why is RAG used in academic assistants?',
            'It improves the accuracy of responses by retrieving relevant information from academic',
            'documents before generating the answer.',
            '',
            'RAG retrieves relevant passages from the document and supplies them to the LLM,',
            'which reduces incorrect answers and keeps responses tied to the study material.',
            '',
            'Furthermore, RAG provides transparent provenance through page citations, enabling',
            'students to verify facts directly against course syllabi, textbooks, and notes.'
        ]
    ]
    
    objects = []
    # 1: Catalog
    objects.append(b'<< /Type /Catalog /Pages 2 0 R >>')
    
    # 2: Pages
    page_obj_ids = [3 + i*2 for i in range(len(pages))]
    kids_str = ' '.join(f'{pid} 0 R' for pid in page_obj_ids)
    objects.append(f'<< /Type /Pages /Kids [{kids_str}] /Count {len(pages)} >>'.encode('ascii'))
    
    font_id = 3 + len(pages)*2
    
    for i, lines in enumerate(pages):
        content_id = 4 + i*2
        page_dict = f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>'.encode('ascii')
        objects.append(page_dict)
        
        stream_lines = ['BT', '/F1 12 Tf', '50 730 Td']
        for line in lines:
            clean = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            stream_lines.append(f'({clean}) Tj')
            stream_lines.append('0 -18 Td')
        stream_lines.append('ET')
        stream_data = '\n'.join(stream_lines).encode('latin-1')
        stream_obj = f'<< /Length {len(stream_data)} >>\nstream\n'.encode('ascii') + stream_data + b'\nendstream'
        objects.append(stream_obj)
        
    # Font
    objects.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    
    with open(filepath, 'wb') as f:
        f.write(b'%PDF-1.4\n')
        offsets = []
        for i, obj in enumerate(objects):
            offsets.append(f.tell())
            f.write(f'{i+1} 0 obj\n'.encode('ascii'))
            f.write(obj)
            f.write(b'\nendobj\n')
        xref_offset = f.tell()
        f.write(b'xref\n')
        f.write(f'0 {len(objects)+1}\n'.encode('ascii'))
        f.write(b'0000000000 65535 f \n')
        for offset in offsets:
            f.write(f'{offset:010d} 00000 n \n'.encode('ascii'))
        f.write(b'trailer\n')
        f.write(f'<< /Size {len(objects)+1} /Root 1 0 R >>\n'.encode('ascii'))
        f.write(b'startxref\n')
        f.write(f'{xref_offset}\n'.encode('ascii'))
        f.write(b'%%EOF\n')

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), 'sample_docs', 'unit3_notes.pdf')
    generate_academic_pdf(out_path)
    print(f'Successfully created sample document: {out_path}')
