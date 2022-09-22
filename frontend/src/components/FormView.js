import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: '',
      categories: []
    };
  }

  componentDidMount() {
    $.ajax({
      url: 'http://127.0.0.1:5000/categories', //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
  }

  submitQuestion = (event) => {
    event.preventDefault();
    // $.ajax({
    //   url: 'http://127.0.0.1:5000/questions', //TODO: update request URL
    //   type: 'POST',
    //   dataType: 'json',
    //   contentType: 'application/json',
    //   data: JSON.stringify({
    //     question: this.state.question,
    //     answer: this.state.answer,
    //     difficulty: this.state.difficulty,
    //     category: this.state.category
    //   }),
    //   xhrFields: {
    //     withCredentials: true,
    //   },
    //   crossDomain: true,
    //   success: (result) => {
    //     document.getElementById('add-question-form').reset();
    //     return;
    //   },
    //   error: (error) => {
    //     alert('Unable to add question. Please try your request again');
    //     return;
    //   },
    // });
    const req = {
      method : 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        category: this.state.category,
        difficulty: this.state.difficulty
      })
    }
    fetch('http://127.0.0.1:5000/questions', req).then(res=>res.json())
    
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id='add-form'>
        <h2>Add a New Trivia Question</h2>
        <form
          className='form-view'
          id='add-question-form'
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input type='text' name='question' onChange={this.handleChange} />
          </label>
          <label>
            Answer
            <input type='text' name='answer' onChange={this.handleChange} />
          </label>
          <label>
            Difficulty
            <select name='difficulty' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <label>
            Category
            <select name='category' onChange={this.handleChange}>
              {(this.state.categories).map((item) => {
                return (
                  <option key={item.id} value={item.type}>
                    {item.type}
                  </option>
                );
              })}
            </select>
          </label>
          <input type='submit' className='button' value='Submit' />
        </form>
      </div>
    );
  }
}

export default FormView;
