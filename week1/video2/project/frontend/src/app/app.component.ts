import { Component } from '@angular/core';
import {HttpClient,HttpHeaders,HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Sentiment Analysis Twitter';
  constructor(
    private _http : HttpClient
  ){

  }

  send(event){
   
   let headers  = new HttpHeaders().set('Content-Type', 'text/csv')
   headers.append('charset','utf-8') 
   
   this._http.get('http://127.0.0.1:8000/'+event.value,{observe:'response',responseType: 'arraybuffer',  headers:headers})
   .subscribe((res :any)=>{         
     this.downloadFile(res,'text/csv');
   })
  }
  
  downloadFile(data:any,type:string){
    let blob = new Blob([data],{type});
    let url = window.URL.createObjectURL(blob);
    let pwa  = window.open(url);
    if (!pwa || pwa.closed || typeof pwa.closed == 'undefined'){
      alert('Please disable your Pop-up blocker and try again.');
    }
  }
}
