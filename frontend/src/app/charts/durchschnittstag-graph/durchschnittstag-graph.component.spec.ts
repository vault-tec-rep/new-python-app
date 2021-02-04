import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DurchschnittstagGraphComponent } from './durchschnittstag-graph.component';

describe('DurchschnittstagGraphComponent', () => {
  let component: DurchschnittstagGraphComponent;
  let fixture: ComponentFixture<DurchschnittstagGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DurchschnittstagGraphComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DurchschnittstagGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
