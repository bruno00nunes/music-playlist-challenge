import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { User } from '@app/_models/user';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    constructor(
        private http: HttpClient,
        private router: Router,
        ) {
        this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): User {
        return this.currentUserSubject.value;
    }

    login(data: Object) {
        console.log(data);
        return this.http.post<any>(`${environment.apiUrl}/api/login`, data)
            .pipe(map(response => {
                let user = response['message']
                localStorage.setItem('currentUser', JSON.stringify(user));
                this.currentUserSubject.next(user);
                return user;
            }));
    }

    register(data: Object) {
        return this.http.post<any>(`${environment.apiUrl}/api/register`, data)
            .pipe(map(response => {
                let user = response['message']
                //localStorage.setItem('currentUser', JSON.stringify(user));
                //this.currentUserSubject.next(user);
                return user;
            }));
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(null);
        this.router.navigate(["/"]);
        // return this.http.post<any>(`${environment.apiUrl}/api/logout`, {})
        //     .pipe(map(response => {
        //         return response;
        //     }));
    }
}
