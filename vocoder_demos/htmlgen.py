r"""
    Generate Static HTML required to post on github
"""

from os import listdir
import argparse

front_matter = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Automaticaly generated content, please update scripts/htmlgen.py for any change -->
   <head>
      <meta charset="UTF-8">
      <title align="center">FBWave audio demo"</title>
      <style type="text/css">
        body, input, select, td, li, div, textarea, p {
        	font-size: 11px;
        	line-height: 16px;
        	font-family: verdana, arial, sans-serif;
        }

        body {
        	margin:5px;
        	background-color:white;
        }

        h1 {
        	font-size:16px;
        	font-weight:bold;
        }

        h2 {
        	font-size:14px;
        	font-weight:bold;
        }
      </style>
   </head>
   <body>
      <article>
         <header>
            <h1>FBWave: Efficient and Scalable Neural Vocoders for Streaming Text-To-Speech on the Edge</h1>
         </header>
      </article>

      <div>
      Website license info sheet <a href = https://yolanda-gao.github.io/Interactive-Style-TTS/Interactive_TTS_license.pdf >pdf</a>
      </div>


      <div>
        <h2>Abstract</h2>
        <p> 
	Nowadays more and more applications can benefit from edge-based text-to-speech (TTS). However, most existing TTS models are too computationally expensive and are not flexible enough to be deployed on the diverse variety of edge devices with their equally diverse computational capacities. To address this, we propose FBWave, a family of efficient and scalable neural vocoders that can achieve optimal performance-efficiency trade-offs for different edge devices. FBWave is a hybrid flow-based generative model that combines the advantages of autoregressive and non-autoregressive models. It produces high quality audio and supports streaming during inference while remaining highly computationally efficient. Our experiments show that FBWave can achieve similar audio quality to WaveRNN while reducing MACs by 40x. More efficient variants of FBWave can achieve up to 109x fewer MACs while still delivering acceptable audio quality.
        </p> 
      </div>
      <h2> Contents </h2>
        <p>
	For faster loading, we only show 10 audio samples per model on this page. More audio samples can be downloaded from <a href = https://github.com/bichenwu09/bichenwu09.github.io </a>here.
        </p>
"""

back_matter = r"""
   </body>
</html>
"""


def get_row_column(root='./fbw-scaling', num_items=10):
    Columns = [x for x in listdir(root) if x[0] != '.']
    assert len(Columns) > 0, 'No subfolders under Asset/'
    Rows = sorted(listdir(f"{root}/{Columns[0]}"))[:num_items]
    # for c in Columns:
    #     assert set(listdir(f"{root}/{c}")) == num_items
    return Rows, Columns


def gen_table_header(name='noname', cols=["nothing"], file=None):
    print(f"""
    <div>
    <h2> {name} </h2>
      <table border = "1" class="inlineTable">
    """, file=file)
    print(
        ''.join([r"""
        <col width="300">""" for _ in cols]),
        file=file)
    print(
        """     <tr> """, file=file)
    print(
        ''.join([f"""
        <th>{col}</th>""" for col in cols]) +
        """ 
</tr>""", file=file)


def audio_entry(audio, file=None):
    print(
        f"""
    <td>
        <audio controls style="width: 200px;">
        <source src={audio} type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </td>""", file=file)


def text_entry(text, file=None):
    print(
        f"""
        <th>{text}</th>""",
        file=file)


def single_row(columns, text=True, file=None):
    print("<tr>", file=file)
    for c in columns:
        if(text):
            text_entry(c, file=file)
        else:
            audio_entry(c, file=file)
    print("</tr>", file=file)


def gen_table(args, file=None):
    for t in args.table:
        rows, cols = get_row_column(t)
        gen_table_header(name=t, cols=cols, file=file)
        for r in rows:
            c = [f"./{t}/{x}/{r}" for x in cols]
            single_row(c, text=args.name_only, file=file)
        print("""
            </table>
        </div>
        """, file=file)


def main(args):
    fname = args.output
    with open(fname, 'w') as f:
        print(front_matter, file=f)
        gen_table(args, file=f)
        print(back_matter, file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--output', type=str,
                        default='index.html', help='output name')
    parser.add_argument('-n', '--name_only',
                        action="store_true", help='put file names only')
    parser.add_argument('-t', '--table', type=str, action="append",
                        nargs='+', help='names of tables', default=['fbw-scaling', 'baselines'])

    args = parser.parse_args()

    main(args)
