#!flask/bin/python
# ! /usr/bin/env python
# coding=utf-8
from flask import Flask, jsonify, abort, request, render_template, redirect, url_for, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename
from app import app
import json
import os
from jtnltk import qacorpus, frequency, synonymy
from forms import myForm


@app.route('/')
@app.route('/index/')
def index():
    form = myForm()
    return render_template('index.html', form=form)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = myForm()
    if request.method == 'GET':
        return redirect('/index/')
    elif request.method == 'POST':
        fil = request.files['file']
    fname = secure_filename(fil.filename)
    # save_path = app.config['UPLOAD_FOLDER']
    if fname.strip() == '':
        flash("Please select file.")
        return redirect('/index/')
    if 'xlsx' in fname or 'xls' in fname:
        fname = 'tmp.xlsx'
        save_path = app.config['TMP_FOLDER']
        fil.save(os.path.join(save_path, fname))
        return redirect('/select_column/')
    elif '.xml' in fname:
        fname = 'tmp.xml'
        save_path = app.config['TMP_FOLDER']
        fil.save(os.path.join(save_path, fname))
        return redirect('/process/')
    else:
        fname = 'rawtext.txt'
        save_path = app.config['TMP_FOLDER']
        fil.save(os.path.join(save_path, fname))
        return redirect('/process/')


@app.route('/select_column/', methods=['GET', 'POST'])
def select_column():
    form = myForm()
    if request.method == 'POST':
        if form.colnum.data != '':
            qacorpus.getrawtext(columnnum=int(form.colnum.data) - 1)
            return redirect('/process')
        else:
            flash("Please select column." + form.colnum.data)
            return render_template('xls.html', form=form, )

    return render_template('xls.html', form=form, )


@app.route('/result/<filename>', methods=['GET'])
def download_file(filename):
    re = open('app/result/' + filename, 'w')
    re.write(open(os.path.join(app.config['TMP_FOLDER'], filename)).read())
    re.close()
    uploads = os.path.join(app.root_path, 'result')
    # print uploads
    return send_from_directory(directory = uploads, filename = filename, as_attachment = True)


@app.route('/process/', methods=['GET', 'POST'])
def process():
    form = myForm()
    link = ''
    label = ''
    if request.method == 'GET':
        return render_template('process.html', form=form, link='', label='')
    if request.method == 'POST':
        label = 'DownloadResult'
        rawtext = open(os.path.join(
            app.config['TMP_FOLDER'], 'rawtext.txt')).readlines()
        if form.fre.data == 'ex':
            link = u'/result/rawtext.txt'
        elif form.fre.data == 'fr':
            qacorpus.frequency(rawtext)
            link = u'/result/frequency.txt'
        elif form.fre.data == 'al':
            synonymy.get_wiki_synonymy(rawtext)
            link = u'/result/aliases.txt'
        elif form.fre.data == 'sy':
            synonymy.get_hit_synonymy(rawtext)
            link = u'/result/synonymy.txt'
        elif form.fre.data == 'xml':
            frequency.statistics()
            link = u'/result/CfgKeywordWeight.properties'
    return render_template('process.html', form=form, link=link, label=label)


@app.route('/frequency', methods=['POST'])
def create_task():
    # print json.dumps(request.json)
    if not request.json or not 'content' in request.json:
        abort(400)
    num, worddict = frequency.statistics(request.json['content'])
    # print len(worddict)
    task = {
        'Number': num,
        'Weight': worddict
    }
    # tasks.append(task)
    return jsonify({'result': task}), 201


@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    if request.files:
        f = request.files['file']
        f.save('tmp/tmp.xlsx')
        return 'upload file successfully!', 201
    else:
        abort(400)


@app.route('/getrawtext', methods=['POST'])
def getrawtext():
    # print json.dumps(request.json)
    lines = []
    if request.json:
        lines = qacorpus.getrawtext(columnnum=request.json['colnum'] - 1)
    else:
        abort(400)
    task = {
        'lines': lines,
    }
    return jsonify({'result': task}), 201


@app.route('/getfrequency', methods=['POST'])
def getfrequency():
    lines = []
    if request.json:
        lines = qacorpus.get_xlsx_frequency(
            columnnum=request.json['colnum'] - 1)
    else:
        abort(400)
    task = {
        'lines': lines,
    }
    return jsonify({'result': task}), 201


@app.route('/getsynonymy', methods=['POST'])
def getsynonymy():
    lines = []
    if request.json:
        lines = synonymy.get_wiki_synonymy(request.json['wordlist'])
    else:
        abort(400)
    task = {
        'lines': lines,
    }
    return jsonify({'result': task}), 201
