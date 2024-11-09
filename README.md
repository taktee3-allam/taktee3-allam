Here's the modified README with the updated repository URL:

---

# taktee3-allam

Project demonstrating how the Taktee3 algorithm leverages Retrieval-Augmented Generation (RAG) to enhance the capabilities of the Allam LLM.

## Demo

- **FrontEnd**: [https://taktee3-allam.vercel.app](https://taktee3-allam.vercel.app)
- **Backend and Scripts**:
  - **Evaluation & Benchmarking Script**: [evaluateLLM.py](https://github.com/taktee3-allam/taktee3-allam/blob/main/datasets/evaluateLLM.py)
  - **Dataset for Fine-tuning**: [poems_data_1.json](https://github.com/taktee3-allam/taktee3-allam/blob/main/datasets/poems_data_1_ready.json)
  - **Dataset for Benchmarking**: [poems_data.csv](https://github.com/taktee3-allam/taktee3-allam/blob/main/datasets/poems_data.csv)

## How to Run

### Frontend

```sh
cd frontend
npm install
npm run build
```

### Backend

Navigate to the `flask_app` directory and run the main API server:

```sh
cd ../flask_app
python main.py
```

### Running Python Scripts

1. **Evaluation & Benchmarking Script**

   This script evaluates the LLM model's performance on provided datasets.

   ```sh
   python datasets/evaluateLLM.py
   ```

   *Ensure you have all required packages installed by checking the `requirements.txt` file.*

2. **Fine-Tuning and Benchmarking Datasets**

   These datasets can be used to further fine-tune or benchmark the model. Use `poems_data_1.json` for fine-tuning and `poems_data.csv` for benchmarking.

## Sample Data Format

Below is an example of the data format used for fine-tuning (`poems_data_1_ready.json`) and benchmarking (`poems_data.csv`):

### Fine-Tuning Data (`poems_data_1_ready.json`)

```json
 {
        "messages": [
            {
                "role": "system",
                "content": "انت مساعد شخصي تستطيع معرفة البحر الشعري لاي بيت شعر؟"
            },
            {
                "role": "user",
                "content": "ما هو البحر الشعري لهذا البيت أَلا مَن مُبلِغُ الأَحلافِ عَنِّي - \nفَقَد تُهدَى النَصيحة للنصيحِ?"
            },
            {
                "role": "assistant",
                "content": "الوافر"
            }
        ]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "انت مساعد شخصي تستطيع معرفة البحر الشعري لاي بيت شعر؟"
            },
            {
                "role": "user",
                "content": "ما هو البحر الشعري لهذا البيت \nفأنَّكم وما تُزجُونَ نحوي - \nمِنَ القَولِ المُرَغَّى والصَريحِ?"
            },
            {
                "role": "assistant",
                "content": "الوافر"
            }
        ]
    },
```

### Benchmarking Data (`poems_data.csv`)

```markdown
## Sample Data

| id  | question | choices| answerKey | source |
| 2000 | ما هو البحر الشعري لهذا البيت أَلا مَن مُبلِغُ الأَحلافِ عَنِّي - فَقَد تُهدَى النَصيحة للنصيحِ? | {'text': ['الوافر', 'مجزوء المنسرح', 'الرمل', 'تفعيلة الرمل'], 'label': ['A', 'B', 'C', 'D']} | A         | [aldiwan.net/poem22](https://www.aldiwan.net/poem22.html) |
| 2002 | ما هو البحر الشعري لهذا البيت فأنَّكم وماتُزجُونَنحوي - مِنَ القَولِالمُرَغَّىوالصَريحِ?           | {'text': ['الوافر', 'منهوك البسيط', 'مجزوء البسيط', 'القوما'], 'label': ['A', 'B', 'C', 'D']} | A         | [aldiwan.net/poem22](https://www.aldiwan.net/poem22.html) |
| 2004 | ما هو البحر الشعري لهذا البيت سَيَندَمُ بَعضُكُم عَجلاً عليه - وما أَثرى اللِسانُ إِلى الجَرُوحِ?     | {'text': ['الوافر', 'المجتث', 'تفعيلة الرجز', 'الطويل'], 'label': ['A', 'B', 'C', 'D']}       | A         | [aldiwan.net/poem22](https://www.aldiwan.net/poem22.html) |
| 2006 | ما هو البحر الشعري لهذا البيت زَعَمَ البُغاثُ أَنَّهم شَجَرُ السِدر - وَلَم أَسِر في دَوحَةِ الزَمانِ? | {'text': ['الكامل', 'الخفيف', 'الطويل', 'الوافر'], 'label': ['A', 'B', 'C', 'D']}            | B         | [aldiwan.net/poem24](https://www.aldiwan.net/poem24.html) |
```

### Explanation

- Use `|` to separate columns and `---` for the header separator.
- For links, use `[text](URL)` to make the `source` URLs clickable.
  
This table will display neatly on GitHub, giving a clear and accessible format for readers.

## YouTube Overview

Watch this video to get an overview of the Taktee3-Allam project:

<iframe width="560" height="315" src="https://www.youtube.com/embed/uMyCxF7xnvs?autoplay=1" title="Taktee3-Allam Overview" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
[Or here](https://www.youtube.com/watch?v=Bbkxwg8MUlY) |
