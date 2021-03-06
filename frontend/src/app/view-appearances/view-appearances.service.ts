import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ListAppearancesService {
  baseurl = environment.apiURL;
  httpHeaders = new HttpHeaders({'Content.Type': 'application/json'});
  constructor(private http: HttpClient) { }
  getAcceptedAppearances(): Observable<any> {
    return this.http.get(this.baseurl + "appearances/status/Accepted/" );
  }
  getAssignedAppearances(sID: Number): Observable<any> {
    return this.http.get(this.baseurl + "listAppearances/status/Assigned/" + sID + "/");
  }
  getID(id: number): Observable<any> {
    return this.http.get(this.baseurl + "appearances/" + id);
  }
  getAppearances(): Observable<any> {
    return this.http.get(this.baseurl + "appearances/status/Assigned" );
  }
}
