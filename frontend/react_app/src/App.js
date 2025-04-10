import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState([]);
  const [wordCloudUrl, setWordCloudUrl] = useState("");
  //const [summary, setSummary] = useState("");
  //const [loading, setLoading] = useState(false);
  
  const fetchData = () => {
    fetch('http://127.0.0.1:5000/api/executive-orders')
  .then(response => response.json())
  .then(data => setData(data))
  .catch(error => console.error('Error fetching data:', error));
  };
  const fetchWordCloud=()=>{
    setWordCloudUrl('http://127.0.0.1:5000/api/wordcloud');
  }
  useEffect(() => {
    console.log("hey")
    fetchData();
    
    fetchWordCloud();
    console.log(wordCloudUrl);

    const interval = setInterval(() => {
      fetchData();}, 5*60*1000); // Fetch data every 60 seconds
      return () => {clearInterval(interval);}; // Clear the interval when the component unmounts
    }, []);
    useEffect(() => {
      console.log("Word Cloud URL updated:", wordCloudUrl);
    }
    ,[wordCloudUrl]);
  /*const fetchSummary = (url) => {
    setLoading(true);
    fetch('/api/summarize',{
      method:'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({url})
    })
    .then((response) => response.json())
    .then((data) => {
      setSummary(data.summary);
      setLoading(false);
    })
    .catch((error) => {
      console.error('Error summarizing:', error);
      setLoading(false);
      setSummary("Error summarizing the executive order.");
    });*/
   // Empty dependency array to run only once on mount
  return (
    <div>
      <h1>Executive Orders</h1>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Executive Order Number</th>
            <th>Signing Date</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key = {index}>  
              <td>{item.title}</td>
              <td>{item.executive_order_number}</td>
              <td>{item.signing_date}</td>
              <td>
                <a href ={item.html_url} target="_blank" rel="noopener noreferrer">
                  More Info</a>
              </td>
              </tr>
          ))}
        </tbody>
      </table>
      <div>
        <h2>Word Cloud</h2>
        {wordCloudUrl&&(
          <img src={wordCloudUrl} alt="Word Cloud" style = {{maxWidth:'100%', height:'auto'}}/>
        )}
      </div>
    </div>
  );
}


export default App;
