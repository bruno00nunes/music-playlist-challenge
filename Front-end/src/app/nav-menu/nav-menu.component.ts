import { Component, Injectable, Inject } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { sha512 } from 'js-sha512';
import { trigger, transition, animate, style } from '@angular/animations'

import { environment } from '@environments/environment';
import { AuthenticationService } from '@app/_services/authentication.service';

import { User } from '@app/_models/user';
import { Plan } from '@app/_models/plan';

@Component({
  selector: 'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls: ['./nav-menu.component.css'],
  animations: [
    trigger('slideUp', [
      transition(':enter', [
        style({transform: 'translateY(100%)'}),
        animate('200ms ease-in', style({transform: 'translateY(0%)'}))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({transform: 'translateY(100%)'}))
      ])
    ])
  ]
})
export class NavMenuComponent {
  isExpanded = false;
  currentPopup = "none";
  Scope = this;
  currentUser: User;
  userMenuVisible = false;
  plans: Plan[];
  planID: number;

  constructor(
    private toastr: ToastrService,
    private http: HttpClient,
    private authenticationService: AuthenticationService
  ) {
    this.authenticationService.currentUser.subscribe(user => this.currentUser = user);
  } 

  ngOnInit(){
    this.userMenuVisible = false;

    // TODO: Add API response model
    // TODO: Make a better select and dynamic request to API
    this.http.get<any>(`${environment.apiUrl}/api/plans/`).subscribe(result => {
      this.plans = result["message"];
    }, error => console.error(error));
  }

  loginSubmit(f: NgForm) {
    let data = f.value;

    if (data["Email"] == null || data["Email"] == '' || data["Password"] == null || data["Password"] == '') {
      this.showErrorMessage("Please insert email and password");
      return;
    }

    let valid = this.validateLoginForm(f);
    if (valid != "Continue") {
      this.showErrorMessage(valid);
      return;
    }

    // let encryptedPassword = sha512.create().update(data["Password"]).hex();

    // this.authenticationService.login(data["Email"], encryptedPassword).subscribe(
    this.authenticationService.login({ "Email": data["Email"], "Password": data["Password"] }).subscribe(
      response => {
        this.toastr.success("You are now logged in!", "Login successful");
        this.currentPopup = "none";
      },
      error => {
        this.showErrorMessage(error);
      }
    );
  }

  registerSubmit(f: NgForm) {
    let data = f.value;
    let valid = this.validateRegistForm(f);
    if (valid != "Continue") {
      this.showErrorMessage(valid);
      return;
    }

    this.authenticationService.register({ "Email": data["email"], "Password": data["password"], "PlanID": data["PlanID"] }).subscribe(
      response => {
        this.toastr.success("Please Confirm your email.", "Registration successful");
        this.currentPopup = "none";
      },
      error => {
        this.showErrorMessage(error);
      }
    );
  }

  logout() {
    this.authenticationService.logout();
    
    this.userMenuVisible = false;
    this.toastr.success("You are now logged out!", "Bye Bye");
    this.currentPopup = "none";
  }

  showErrorMessage(message: string) {
    this.toastr.error(message, 'Error');
  }

  validateLoginForm(f: NgForm) {
    return this.validateForm([this.validateEmail], f);
  }

  validateRegistForm(f: NgForm) {
    return this.validateForm([this.validateEmail, this.validatePassword], f);
  }

  validateForm(validations, f: NgForm) {
    let validationResult = "Continue";
    for (let i = 0; i < validations.length; i++) {
      validationResult = validations[i](f);
      if (validationResult !== "Continue") {
        return validationResult;
      }
    }
    return validationResult;
  }

  validatePassword = (function (f: NgForm) {
    // //Rules -> must contain 1 Uppercase, must contain lowercase, must contain number, lenght >= 6, must be equal to confirmation password
    // let regex_validation = /^(?!.*[\s])(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{6,}$/;
    // if (f.value["password"] != f.value["confirmpassword"]) {
    //   return "Passwords must match";
    // }
    // let validation = (regex_validation.test(f.value["password"])) ? ("Continue") : ("Invalid Password");
    // if (validation != "Continue") {
    //     this.toastr.info("<ul><li>Passwords must contain one Uppercase letter, one lowercase letter, one number and at least 6 characters</li><li>Cannot contain whitespaces</li><li>Valid characters are between a-Z and _</li></ul>", 'Information', {timeOut: 5000});
    // }
    // return validation;
    return true
  }).bind(this);

  validateEmail(f: NgForm) {
    //Rules -> x@x.xx
    let regex_validation = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
    return (regex_validation.test(f.value["Email"])) ? ("Continue") : ("Invalid Email");
  }
}
